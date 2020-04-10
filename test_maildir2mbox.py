import unittest, pathlib, logging

from maildir2mbox import convert, configure

class TestMaildir2Mbox(unittest.TestCase):

    def setUp(self):
        self.mbox_name = pathlib.Path('test_data/mbox_toto')
        self.mbox_dir  = pathlib.Path('test_data/mbox_toto.sbd')
        # start witha a clean environment
        self.tearDown()

    def tearDown(self):
        if self.mbox_name.exists():
            self.mbox_name.unlink()
        if self.mbox_dir.exists():
            self.mbox_dir.rmdir()

    def test_convert_non_existing_dir(self): 
        self.assertEqual( convert('test_data/i_do_not_exist', str(self.mbox_name)) , 1 )
        self.assertEqual( self.mbox_name.exists(), False)

    def test_convert_non_maildir_dir(self): 
        tmp_dir = pathlib.Path('test_data/tmp_dir')
        tmp_dir.mkdir()
        try:
            self.assertEqual( convert(str(tmp_dir), str(self.mbox_name)) , 1 )
        finally:
            tmp_dir.rmdir()

        tmp_new = tmp_dir/'new'

        tmp_dir.mkdir()
        tmp_new.mkdir()
        try:
            self.assertEqual( convert(str(tmp_dir), str(self.mbox_name)) , 1 )
        finally:
            tmp_new.rmdir()
            tmp_dir.rmdir()


        tmp_cur = tmp_dir/'cur'
        tmp_dir.mkdir()
        tmp_cur.mkdir()
        try:
            self.assertEqual( convert(str(tmp_dir), str(self.mbox_name)) , 1 )
        finally:
            tmp_cur.rmdir()
            tmp_dir.rmdir()


    def test_successful_conversion(self): 
        self.assertEqual( convert('test_data/.INBOX.toto', str(self.mbox_name)) , 0 )
        self.assertEqual( self.mbox_name.exists(), True)
        self.assertEqual( self.mbox_name.is_file(), True)
        self.assertEqual( self.mbox_dir.exists(), True)
        self.assertEqual( self.mbox_dir.is_dir(), True)

        with open(self.mbox_name) as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: toto read'), 1)
            self.assertEqual( mbox_content.count('Subject: toto unread'), 1)

    def test_appending_to_existing_mbox(self): 
        self.assertEqual( convert('test_data/.INBOX.toto', str(self.mbox_name)) , 0 )
        self.assertEqual( convert('test_data/.INBOX.toto.titi', str(self.mbox_name)) , 0 )

        with open(self.mbox_name) as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 4)
            self.assertEqual( mbox_content.count('Subject: toto read'), 1)
            self.assertEqual( mbox_content.count('Subject: toto unread'), 1)
            self.assertEqual( mbox_content.count('Subject: titi read'), 1)
            self.assertEqual( mbox_content.count('Subject: titi unread'), 1)

if __name__ ==  '__main__':
    configure()
    unittest.main(verbosity=True)