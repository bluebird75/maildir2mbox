[![Build Status](https://travis-ci.org/bluebird75/maildir2mbox.svg?branch=master)](https://travis-ci.org/bluebird75/maildir2mbox)

maildir2mbox
============

Convert mailbox from maildir format to mbox format, with support for nested folders

Improvements by Philippe Fremy:
- porting to Python 3 to deal with filesystem encoding problems: works when moving maildir data from a partition 
  supporting utf8 filenames (Ext3) to a partition supporting mbcs filenames (ntfs)
- argument handling and help display
- add support for nested directories
- move to GitHub

Authors:
    Philippe Fremy, April 2013-2020
    Frédéric Grosshans, 19 January 2012
    Nathan R. Yergler, 6 June 2010

Very first version from:
	http://yergler.net/blog/2010/06/06/batteries-included-or-maildir-to-mbox-again/
	Adapted from maildir2mbox.py, Nathan R. Yergler, 6 June 2010:

This file does not contain sufficient creative expression to invoke
assertion of copyright. No warranty is expressed or implied; use at
your own risk.

