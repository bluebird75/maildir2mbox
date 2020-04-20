"""
The file is under no license. See LICENSE.txt for more details.
"""

import unittest, shutil, sys
from pathlib import Path

from maildir2mbox import convert

class TestMaildir2Mbox(unittest.TestCase):

    def setUp(self):
        self.mbox_path          = Path('test_data/mbox_toto')
        self.mbox_dir           = Path('test_data/mbox_toto.sbd')
        self.mbox_titi_path     = Path('test_data/mbox_toto.sbd/titi')
        self.mbox_titi_dir      = Path('test_data/mbox_toto.sbd/titi.sbd')
        self.mbox_tutu_path     = Path('test_data/mbox_toto.sbd/titi.sbd/tutu')
        self.mbox_tutu_dir      = Path('test_data/mbox_toto.sbd/titi.sbd/tutu.sbd')
        self.many_path          = Path('test_data/mbox_many')
        self.many_dir           = Path('test_data/mbox_many.sbd')
        self.mbox_coincoin_path = Path('test_data/mbox_toto.sbd/coincoin')
        self.mbox_coincoin_dir  = Path('test_data/mbox_toto.sbd/coincoin.sbd')
        self.mbox_coucou_path   = Path('test_data/mbox_toto.sbd/coincoin.sbd/coucou')
        self.mbox_coucou_dir    = Path('test_data/mbox_toto.sbd/coincoin.sbd/coucou.sbd')
        # start witha a clean environment
        self.tearDown()

    def tearDown(self):
        for f in [self.mbox_path, self.mbox_titi_path, self.mbox_tutu_path, self.many_path,
                    self.mbox_coucou_path, self.mbox_coincoin_path]:
            if f.exists():
                f.unlink()
        for d in [self.mbox_tutu_dir, self.mbox_titi_dir, self.mbox_dir, self.many_dir,
                    self.mbox_coincoin_dir, self.mbox_coucou_dir]:
            if d.exists():
                shutil.rmtree(str(d))

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

        self.assertEqual(self.mbox_coincoin_path.exists(), True)
        self.assertEqual(self.mbox_coincoin_path.is_file(), True)
        self.assertEqual(self.mbox_coincoin_dir.exists(), True)
        self.assertEqual(self.mbox_coincoin_dir.is_dir(), True)

        self.assertEqual(self.mbox_coucou_path.exists(), True)
        self.assertEqual(self.mbox_coucou_path.is_file(), True)
        self.assertEqual(self.mbox_coucou_dir.exists(), True)
        self.assertEqual(self.mbox_coucou_dir.is_dir(), True)

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

        with self.mbox_coincoin_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: coincoin read'), 1)
            self.assertEqual( mbox_content.count('Subject: coincoin unread'), 1)

        with self.mbox_coucou_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 2)
            self.assertEqual( mbox_content.count('Subject: coucou read'), 1)
            self.assertEqual( mbox_content.count('Subject: coucou unread'), 1)


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

class TestMaildir2MboxLongExecution(TestMaildir2Mbox):

    def test_conversion_1000_msg(self): 
        self.assertEqual( convert(Path('test_data/.many_messages'), self.many_path, False) , 0 )
        self.assertEqual( self.many_path.exists(), True)
        self.assertEqual( self.many_path.is_file(), True)

        with self.many_path.open() as f:
            mbox_content = f.read()
            self.assertEqual( mbox_content.count('From '), 999)
            self.assertEqual( mbox_content.count('Subject: tutu 001 read'), 1)
            self.assertEqual( mbox_content.count('Subject: tutu 999 read'), 1)


if __name__ ==  '__main__':
    tests_to_run = ['TestMaildir2Mbox']
    argv = sys.argv[:]
    if '--long-tests' in argv:
        tests_to_run.append('TestMaildir2MboxLongExecution')
        del argv[argv.index('--long-tests')]

    unittest.main(verbosity=True, defaultTest=tests_to_run, argv=argv)
    