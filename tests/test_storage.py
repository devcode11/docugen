from unittest import TestCase
from docugen.storage import FileStore
import tempfile
import shutil
from pathlib import Path

class FileStoreTests(TestCase):
    def setUp(self):
        self.testdir_path = tempfile.mkdtemp(prefix='docugen_testdir')
        self.file_store = FileStore(rootdir=self.testdir_path, dir_file_name='summary_for_directory.md')

    def tearDown(self):
        shutil.rmtree(self.testdir_path)

    def assert_file_contents(self, file_path: str, file_summary: str):
        path = Path(self.testdir_path, file_path)
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())
        self.assertEqual(file_summary, path.read_text())

    def test_store_summary_file_creates_file(self):
        file_path = 'abc/def/file1.py'
        file_summary = 'This file is for testing'
        self.file_store.store_summary(file_path, file_summary, is_dir=False)
        self.assert_file_contents(file_path, file_summary)

    def test_store_summary_directory_creates_file(self):
        dir_path = 'abc/def/dir1'
        dir_summary = 'This dir is for testing'
        self.file_store.store_summary(dir_path, dir_summary, is_dir=True)
        self.assert_file_contents(dir_path + '/summary_for_directory.md', dir_summary)

    def test_get_summary_directory_reads_from_directory_file(self):
        dir_path = 'abc/def/dir1'
        dir_summary = 'This dir is for testing read'
        path = Path(self.testdir_path, dir_path, 'summary_for_directory.md')
        path.parent.mkdir(parents=True, exist_ok = True)
        path.write_text(dir_summary)
        fetched_summary = self.file_store.get_summary(dir_path, is_dir=True)
        self.assertEqual(dir_summary, fetched_summary)

    def test_get_summary_file_reads_from_file(self):
        file_path = 'abc/def/file1.py'
        file_summary = 'This file is for testing read'
        path = Path(self.testdir_path, file_path)
        path.parent.mkdir(parents=True, exist_ok = True)
        path.write_text(file_summary)
        fetched_summary = self.file_store.get_summary(file_path, is_dir=False)
        self.assertEqual(file_summary, fetched_summary)
