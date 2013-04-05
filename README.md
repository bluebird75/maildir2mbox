maildir2mbox
============

Convert mailbox from maildir format to mbox format. Handles nested folders and fs encoding problems.
Works only with Python 3. Python 2 version available at the original location.

Copied from:
http://stackoverflow.com/questions/2501182/convert-maildir-to-mbox

Improvements by Philippe Fremy:
- porting to Python 3 to deal with filesystem encoding problems: works when moving maildir data from a partition 
  supporting utf8 filenames (Ext3) to a partition supporting mbcs filenames (ntfs)
- argument handling and help display
