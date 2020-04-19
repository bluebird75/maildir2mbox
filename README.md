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

To install:
- either download directly the maildir2mbox.py file and execute it:

	```$ python maildir2mbox.py --help```

- or install with pip, then run it with -m:
```	
	$ pip install maildir2mbox
	$ python -m maildir2mbox --help
```

Authors:
- Philippe Fremy, April 2013-2020
- Frédéric Grosshans, 19 January 2012
- Nathan R. Yergler, 6 June 2010

The file is under no license/public domain. See LICENSE.txt for more details.

