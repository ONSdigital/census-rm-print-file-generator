import csv

import responses

from process_sample_file import process_sample_file_from_path
from tests import CleanupOutputsTestCase, IACConfigTestCase


class TestProcessSampleFile(IACConfigTestCase, CleanupOutputsTestCase):
    iac_batch = ['testiaccode1', 'testiaccode2', 'testiaccode3', 'testiaccode4', 'testiaccode5']

    def test_process_sample_file_from_path(self):
        sample_file_path = self.test_resources_dir.joinpath('sample_5.csv')
        processed_file_path = self.test_output_dir.joinpath('test_process_sample_file_from_path.csv')
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=self.iac_batch)
            process_sample_file_from_path(sample_file_path,
                                          processed_file_path)

        with open(processed_file_path) as processed_file, open(sample_file_path) as sample_file:
            processed_file_reader = csv.DictReader(processed_file)
            sample_file_reader = csv.DictReader(sample_file)

            for row in processed_file_reader:
                assert all(row[key] == value for key, value in next(sample_file_reader).items())
                assert row['CASE_REF']
                assert row['QID']
                assert row['UAC'] in self.iac_batch
