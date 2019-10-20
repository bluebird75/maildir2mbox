#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
u"""
Frédéric Grosshans, 19 January 2012
Nathan R. Yergler, 6 June 2010
Philippe Fremy, April 2013

This file does not contain sufficient creative expression to invoke
assertion of copyright. No warranty is expressed or implied; use at
your own risk.

---

Uses Python's included mailbox library to convert mail archives from
maildir [http://en.wikipedia.org/wiki/Maildir] to 
mbox [http://en.wikipedia.org/wiki/Mbox] format, including subfolders.

See https://docs.python.org/3/library/mailbox.html#mailbox.Mailbox for 
full documentation on this library.
"""

HELP=u"""
$ python maildir2mbox.py [maildir_path] [mbox_filename]

[maildir_path] should be the the path to the actual maildir (containing new, 
cur, tmp, and the subfolders, which are hidden directories with names like 
.subfolde.subsubfolder.subsubsbfolder);

[mbox_filename] will be newly created, as well as a [mbox_filename].sbd 
directory.
"""

import mailbox
import sys
import email
import os
import traceback

def maildir2mailbox(maildirname, mboxfilename):
    """
    slightly adapted from maildir2mbox.py, 
    Nathan R. Yergler, 6 June 2010
    http://yergler.net/blog/2010/06/06/batteries-included-or-maildir-to-mbox-again/
    Port to Python 3 by Philippe Fremy
    """
    # open the existing maildir and the target mbox file
    maildir = mailbox.Maildir(maildirname, email.message_from_binary_file)
    mbox = mailbox.mbox(mboxfilename)

    # lock the mbox
    # mbox.lock()

    # iterate over messages in the maildir and add to the mbox
    n = len(maildir)
    for i, v in enumerate(maildir.iteritems()):
        key, msg = v
        if (i % 10) == 9:
            print( 'Progress: msg %d of %d' % (i+1,n))
        try:
            mbox.add(msg)
        except Exception:
            print( 'Exception while processing msg with key: %s' % key )
            traceback.print_exc()            

    # close and unlock
    mbox.close()
    maildir.close()


if __name__ == '__main__':
    if sys.version_info[:2] < (3,2):
        print( 'This program needs at least Python 3.2 to work' )
        sys.exit(0)

    if len(sys.argv) < 3:
        print( HELP )
        sys.exit(0)

    #Creates the main mailbox
    dirname=sys.argv[-2]
    mboxname=sys.argv[-1]
    print(dirname +' -> ' +mboxname)
    mboxdirname=mboxname+'.sbd'
    maildir2mailbox(dirname,mboxname)
    if not os.path.exists(mboxdirname): os.makedirs(mboxdirname)

    listofdirs=[dirname for dirinfo in os.walk(dirname) 
                            for dirname in dirinfo[1] 
                                if dirname not in ['new', 'cur', 'tmp'] and
                                    dirname.startswith('.') ]
    for curfold in listofdirs:
        curlist=[mboxname]+curfold.split('.')
        curpath=os.path.join(*[dn+'.sbd' for dn in curlist if dn])
        if not os.path.exists(curpath): os.makedirs(curpath)
        print('| ' +curfold +' -> '+curpath[:-4])
        maildir2mailbox(os.path.join(dirname,curfold),curpath[:-4])

    print('Done')



