import os
import unittest
from pathlib import Path


class IACConfigTestCase(unittest.TestCase):
    test_iac_url = 'http://test'

    def setUp(self) -> None:
        super().setUp()
        os.environ['IAC_URL'] = self.test_iac_url
        os.environ['IAC_USERNAME'] = 'test_user'
        os.environ['IAC_PASSWORD'] = 'test_password'


class CleanupFilesTestCase(unittest.TestCase):
    test_output_directory = Path(__file__).parent.resolve().joinpath('tmp_test_files')
    test_resources_directory = Path(__file__).parent.resolve().joinpath('resources')

    def tear_down_test_output_directory(self) -> None:
        if self.test_output_directory.exists():
            for _file in self.test_output_directory.iterdir():
                _file.unlink()
            self.test_output_directory.rmdir()

    def setUp(self) -> None:
        super().setUp()
        self.tear_down_test_output_directory()
        self.test_output_directory.mkdir()

    def tearDown(self) -> None:
        super().tearDown()
        self.tear_down_test_output_directory()
