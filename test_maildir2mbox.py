"""
The file is under no license. See LICENSE.txt for more details.
"""

import unittest
from pathlib import Path

from maildir2mbox import convert

class TestMaildir2Mbox(unittest.TestCase):

    def setUp(self):
        self.mbox_path = Path('test_data/mbox_toto')
        self.mbox_dir  = Path('test_data/mbox_toto.sbd')
        self.mbox_titi_path = Path('test_data/mbox_toto.sbd/titi')
        self.mbox_titi_dir  = Path('test_data/mbox_toto.sbd/titi.sbd')
        self.mbox_tutu_path = Path('test_data/mbox_toto.sbd/titi.sbd/tutu')
        self.mbox_tutu_dir  = Path('test_data/mbox_toto.sbd/titi.sbd/tutu.sbd')
        # start witha a clean environment
        self.tearDown()

    def tearDown(self):
        for f in [self.mbox_path, self.mbox_titi_path, self.mbox_tutu_path]:
            if f.exists():
                f.unlink()
        for d in [self.mbox_tutu_dir, self.mbox_titi_dir, self.mbox_dir]:
            if d.exists():
                d.rmdir()

    def test_convert_non_existing_dir(self): 
        self.assertEqual( convert(Path('test_data/i_do_not_exist'), self.mbox_path, False) , 1 )
        self.assertEqual( self.mbox_path.exists(), False)

    def test_convert_non_maildir_dir(self): 
        tmp_dir = Path('test_data/tmp_dir')
        tmp_dir.mkdir()
        try:
            self.assertEqual( convert(tmp_dir, self.mbox_path, False) , 1 )
        finally:
            tmp_dir.rmdir()

        tmp_new = tmp_dir/'new'

        tmp_dir.mkdir()
        tmp_new.mkdir()
        try:
            self.assertEqual( convert(tmp_dir, self.mbox_path, False) , 1 )
        finally:
            tmp_new.rmdir()
            tmp_dir.rmdir()


        tmp_cur = tmp_dir/'cur'
        tmp_dir.mkdir()
        tmp_cur.mkdir()
        try:
            self.assertEqual( convert(tmp_dir, self.mbox_path, False) , 1 )
        finally:
            tmp_cur.rmdir()
            tmp_dir.rmdir()


    def test_successful_conversion(self): 
        self.assertEqual( convert(Path('test_data/.INBOX.toto'), self.mbox_path, False) , 0 )
        self.assertEqual( self.mbox_path.exists(), True)
        self.assertEqual( self.mbox_path.is_file(), True)
        self.assertEqual( self.mbox_dir.exists(), True)
        self.assertEqual( self.mbox_dir.is_dir(), True)

        with self.mbox_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: toto read'), 1)
            self.assertEqual( mbox_content.count('Subject: toto unread'), 1)


    def test_successful_conversion_recurse(self): 
        self.assertEqual( convert(Path('test_data/.INBOX.toto'), self.mbox_path, True) , 0 )
        self.assertEqual( self.mbox_path.exists(), True)
        self.assertEqual( self.mbox_path.is_file(), True)
        self.assertEqual( self.mbox_dir.exists(), True)
        self.assertEqual( self.mbox_dir.is_dir(), True)

        self.assertEqual(self.mbox_titi_path.exists(), True)
        self.assertEqual(self.mbox_titi_path.is_file(), True)
        self.assertEqual(self.mbox_titi_dir.exists(), True)
        self.assertEqual(self.mbox_titi_dir.is_dir(), True)

        self.assertEqual(self.mbox_tutu_path.exists(), True)
        self.assertEqual(self.mbox_tutu_path.is_file(), True)
        self.assertEqual(self.mbox_tutu_dir.exists(), True)
        self.assertEqual(self.mbox_tutu_dir.is_dir(), True)

        with self.mbox_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: toto read'), 1)
            self.assertEqual( mbox_content.count('Subject: toto unread'), 1)

        with self.mbox_titi_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: titi read'), 1)
            self.assertEqual( mbox_content.count('Subject: titi unread'), 1)

        with self.mbox_tutu_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: tutu read'), 1)
            self.assertEqual( mbox_content.count('Subject: tutu unread'), 1)


    def test_appending_to_existing_mbox(self): 
        self.assertEqual( convert(Path('test_data/.INBOX.toto'), self.mbox_path, False) , 0 )
        self.assertEqual( convert(Path('test_data/.INBOX.toto.titi'), self.mbox_path, False) , 0 )

        with self.mbox_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 4)
            self.assertEqual( mbox_content.count('Subject: toto read'), 1)
            self.assertEqual( mbox_content.count('Subject: toto unread'), 1)
            self.assertEqual( mbox_content.count('Subject: titi read'), 1)
            self.assertEqual( mbox_content.count('Subject: titi unread'), 1)

if __name__ ==  '__main__':
    unittest.main(verbosity=True)