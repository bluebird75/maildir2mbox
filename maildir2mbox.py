#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uses Python's included mailbox library to convert mail archives from
Maildir [http://en.wikipedia.org/wiki/Maildir] to
mbox [http://en.wikipedia.org/wiki/Mbox] format,
including subfolders, in Mozilla Thunderbird style.

See https://docs.python.org/3/library/mailbox.html#mailbox.Mailbox for
full documentation on this library.

Authors:
    Philippe Fremy, April 2013-2020
    Frédéric Grosshans, 19 January 2012
    Nathan R. Yergler, 6 June 2010

Very first version from: http://yergler.net/blog/2010/06/06/batteries-included-or-maildir-to-mbox-again/

The file is under no license/public domain. See LICENSE.txt for more details.
"""

import os, sys, argparse, mailbox, datetime
from typing import Optional
from  pathlib import Path

def info(*args):
    # type: (*str) -> None
    '''Display informative message'''
    prefix = datetime.datetime.now().time().replace(microsecond=0).isoformat()
    print(prefix, *args)

def error(*args):
    # type: (*str) -> None
    '''Display error message'''
    prefix = datetime.datetime.now().time().replace(microsecond=0).isoformat()
    print('ERROR', prefix, *args)


def maildir2mailbox(maildir_path, mbox_path):
    # type: (Path, Path) -> int

    if not maildir_path.exists():
        error('maildir directory %s does not exist' % maildir_path)
        return 1

    if not ((maildir_path/'cur').exists() and (maildir_path/'new').exists()):
        error('Missing `new` and/or `cur` subdirectories in path %s, aborting conversion' % maildir_path)
        return 1

    mboxdir_path = Path('%s.sbd' % mbox_path)
    if not mboxdir_path.exists():
        mboxdir_path.mkdir(parents=True, exist_ok=True)
    elif mbox_path.is_dir():
        error('%s exists but is not a directory!' % mbox_path)
        return 1

    info('%s -> %s' % (maildir_path, mbox_path))

    maildir = None  # type: Optional[mailbox.Maildir]
    mbox = None     # type: Optional[mailbox.mbox]
    try:
        maildir = mailbox.Maildir(str(maildir_path))
        mails = len(maildir)
        if not mails:
            maildir.close()
            return 0

        if mbox_path.exists():
            info('Using existing mbox file and adding the messages to it.')

        mbox = mailbox.mbox(str(mbox_path))
        mbox.lock()

        # iterate over messages in the maildir and add to the mbox
        info('Processing %d messages in %s' % (mails, maildir_path))
        for i, v in enumerate(maildir.iteritems()):
            key, msg = v
            if (i % 100) == 99:
                info('Progress: msg %d of %d' % (i+1, mails))
            try:
                mbox.add(msg)
            except Exception:
                error('Exception while processing msg with key: %s' % key)
                #traceback.print_exc()
                raise
    finally:
        # close and unlock
        if mbox:
            mbox.close()
        if maildir:
            maildir.close()

    return 0

def convert(maildir_path, mbox_path, recurse):
    # type: (Path, Path, bool) -> int
    """ Convert maildirs to mbox

    maildir_path: path to the maildir directory containing new, cur and tmp directories
    mbox_path: path to the mbox file, already existing or to be created.
    recurse: if True, process also mail subfolders of maildir_path
    """
    # Creates the main mailbox

    result = maildir2mailbox(maildir_path, mbox_path)

    # There are two types of subfolders for maildir format. The official
    # one is that a maildir directory is an official directory if it starts
    # with a dot . Mail subfolders contain the same name a suffix in .[subdirectory_name]
    #
    # Example:
    #   .one_maildir_folder/
    #     + cur/
    #     + new/
    #     + tmp/
    #   .one_maildir_folder.some_subfolder/
    #     + cur/
    #     + new/
    #     + tmp/
    #
    # The other format is less official but also exists in some programs. In this
    # case, the mail subfolder are actually subfolders of the maildir directory.
    #
    # Example:
    #   .one_maildir_folder/
    #      + cur/
    #      + new/
    #      + tmp/
    #      + .some_subfolder/
    #          + cur/
    #          + new/
    #          + tmp/
    #
    # This program supports both formats

    if not recurse:
        return result

    # look for the directories starting just like maildir_path
    mdp_prefix = maildir_path.parts[-1] + '.'
    maildir_sub_path = [ p for p in maildir_path.parent.iterdir()
                            if p.name != mdp_prefix[:-1] and p.name.startswith(mdp_prefix)
                            ]
    maildir_sub_path2 = [p for p in maildir_sub_path 
                        if p.is_dir() and (p/'cur').exists() and (p/'new').exists()]

    # .INBOX.toto
    # .INBOX.toto.titi
    # .INBOX.toto.titi.tutu
    # =>
    # mbox_toto.sbd
    # mbox_toto.sbd/titi.sbd
    # mbox_toto.sbd/titi
    # mbox_toto.sbd/titi.sbd/tutu.sbd
    # mbox_toto.sbd/titi.sbd/tutu
    for subdir in maildir_sub_path2:
        mbox_dir_sub_path = Path(str(mbox_path) + subdir.name[len(mdp_prefix)-1:].replace('.', '.sbd/')+'.sbd')
        mbox_sub_path = Path(str(mbox_dir_sub_path)[:-4])
        mbox_dir_sub_path.mkdir(parents=True, exist_ok=True)
        info('%s -> %s' % (subdir, mbox_sub_path))
        result += maildir2mailbox(subdir, mbox_sub_path)


    # .INBOX.toto/.coincoin
    # .INBOX.toto/.coincoin/.coucou
    # =>
    # mbox_toto.sbd
    # mbox_toto.sbd/coincoin
    # mbox_toto.sbd/coincoin.sbd
    # mbox_toto.sbd/coincoin.sbd/coucou
    # mbox_toto.sbd/coincoin.sbd/coucou.sbd
    mdp_prefix = maildir_path.parts[-1] + '.'
    maildir_sub_path = [ (Path(dirinfo[0])/subdir).relative_to(maildir_path) for dirinfo in os.walk(str(maildir_path))
                                        for subdir in dirinfo[1] 
                                            if subdir.startswith('.') ]
    for subdir in maildir_sub_path:
        mbox_dir_sub_path = Path(str(mbox_path) + '.sbd/' + subdir.as_posix()[1:].replace('/.', '.sbd/')+'.sbd')
        mbox_sub_path = Path(str(mbox_dir_sub_path)[:-4])
        mbox_dir_sub_path.mkdir(parents=True, exist_ok=True)
        result += maildir2mailbox(maildir_path / subdir, mbox_sub_path)

    if result > 0:
        info('Done with %d errors.' % result)
    else:
        info('Done')
    return result

if __name__ == '__main__':
    if sys.version_info[:2] < (3,5):
        sys.stderr.write('This program needs at least Python 3.5 to work\r\n')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('maildir_path',
                        help=("path to the existing maildir "
                              "(containing new, cur, tmp) subdirectories"))
    parser.add_argument('mbox_filename',
                        help=("target filename in the mbox format. If the mailbox already exists, new messages are appended to it." ))
    parser.add_argument('-r', '--recurse', dest='recurse', help="Process all mail folders included in maildir_path. An equivalent "
                        "structure is recreated in the mbox format", 
                        action='store_true')
    args = parser.parse_args()

    sys.exit(
        convert(Path(args.maildir_path), Path(args.mbox_filename), bool(args.recurse))
    )
