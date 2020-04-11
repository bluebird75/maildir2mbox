#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uses Python's included mailbox library to convert mail archives from
Maildir [http://en.wikipedia.org/wiki/Maildir] to
mbox [http://en.wikipedia.org/wiki/Mbox] format,
including subfolders, in Mozilla Thunderbird style.

See https://docs.python.org/3/library/mailbox.html#mailbox.Mailbox for
full documentation on this library.
"""

NOTES = """
Philippe Fremy, April 2013
Frédéric Grosshans, 19 January 2012
Nathan R. Yergler, 6 June 2010

This file does not contain sufficient creative expression to invoke
assertion of copyright. No warranty is expressed or implied; use at
your own risk.
"""

import sys
import os
import argparse
import mailbox
import email
#import traceback
import logging

logger = logging.getLogger(__name__)


def maildir2mailbox(maildirname, mboxfilename):
    """
    Adapted from maildir2mbox.py, Nathan R. Yergler, 6 June 2010:
    http://yergler.net/blog/2010/06/06/batteries-included-or-maildir-to-mbox-again/
    Port to Python 3 by Philippe Fremy
    """

    if not os.path.exists(maildirname):
        logger.error('maildir directory %s does not exist' % maildirname)
        return 1

    if not (os.path.exists(os.path.join(maildirname, 'cur')) and os.path.exists(os.path.join(maildirname, 'new'))):
        logger.error('Missing `new` and/or `cur` subdirectories, aborting conversion')
        return 1


    logger.info('%s -> %s' % (maildirname, mboxfilename))


    maildir = None
    mbox = None
    try:
        maildir = mailbox.Maildir(maildirname, email.message_from_binary_file)
        mails = len(maildir)
        if not mails:
            maildir.close()
            return

        if os.path.exists(mboxfilename):
            logger.info('mbox file already exists, appending the messages')

        mbox = mailbox.mbox(mboxfilename)
        mbox.lock()

        # iterate over messages in the maildir and add to the mbox
        logger.info('Processing %d messages in %s' % (mails, maildirname))
        for i, v in enumerate(maildir.iteritems()):
            key, msg = v
            if (i % 10) == 9:
                logger.debug('Progress: msg %d of %d' % (i+1, mails))
            try:
                mbox.add(msg)
            except Exception:
                logger.error('Exception while processing msg with key: %s' % key)
                mbox.close()
                maildir.close()
                #traceback.print_exc()
                raise
    finally:
        # close and unlock
        mbox.close()
        maildir.close()

    return 0

def convert(maildir_path, mbox_filename):
    """ Convert maildirs to mbox.

    Including subfolders, in Mozilla Thunderbird style.
    """
    # Creates the main mailbox

    mboxdirname = '%s.sbd' % mbox_filename

    if not os.path.exists(mboxdirname):
        os.makedirs(mboxdirname)

    elif not os.path.isdir(mboxdirname):
        logger.error('%s exists but is not a directory!' % mboxdirname)
        return 1

    return maildir2mailbox(maildir_path, mbox_filename)

    # Creates the subfolder mailboxes
    listofdirs = [maildir_path for dirinfo in os.walk(maildir_path)
                                  for dirname in dirinfo[1]
                                      if dirname.startswith('.')]
                                          #and dirname not in ['new', 'cur', 'tmp']]
    for curfold in listofdirs:
        curlist = [mbox_filename] + curfold.split('.')
        curpath = os.path.join(*['%s.sbd' % dn for dn in curlist if dn])
        mboxpath = curpath[:-4]
        if not os.path.exists(curpath):
            os.makedirs(curpath)
        logger.info('| %s -> %s' % (curfold, mboxpath))

        maildir2mailbox(os.path.join(maildir_path, curfold), mboxpath)

    logger.info('Done')
    return 0

def configure():
    logging.basicConfig(format='%(asctime)s [%(levelname)-5s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %Z')
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    if sys.version_info[:2] < (3,2):
        sys.stderr.write('This program needs at least Python 3.2 to work\r\n')
        sys.exit(1)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__, epilog=NOTES)
    parser.add_argument('maildir_path',
                        help=("is the the path to the existing maildir "
                              "(containing new, cur, tmp, and the subfolders, "
                              "which are directories prefixed by a dot)"))
    parser.add_argument('mbox_filename',
                        help=("will be newly created, together with a "
                              "[mbox_filename].sbd directory."))
    parser.add_argument('-v', dest='verbose', help="more verbose output",
                        action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    sys.exit(
        convert(args.maildir_path, args.mbox_filename)
    )
