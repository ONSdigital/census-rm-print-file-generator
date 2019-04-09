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


class CleanupOutputsTestCase(unittest.TestCase):
    test_output_dir = Path(__file__).parent.resolve().joinpath('tmp_test_outputs')
    test_resources_dir = Path(__file__).parent.resolve().joinpath('resources')

    def clear_test_output_directory(self) -> None:
        if self.test_output_dir.exists():
            for file in self.test_output_dir.iterdir():
                file.unlink()
            self.test_output_dir.rmdir()

    def setUp(self) -> None:
        super().setUp()
        self.clear_test_output_directory()
        self.test_output_dir.mkdir()

    def tearDown(self) -> None:
        super().tearDown()
        self.clear_test_output_directory()
