import csv

from generate_print_files import generate_print_files_from_sample_file_path
from tests import CleanupFilesTestCase


class TestGeneratePrintFile(CleanupFilesTestCase):

    def test_generate_print_files_from_sample_file_path(self):
        processed_sample_file_path = self.test_resources_directory.joinpath('processed_sample_5.csv')
        generate_print_files_from_sample_file_path(processed_sample_file_path, self.test_output_directory)

        icl1_print_file_path = next(self.test_output_directory.glob('P_IC_ICL1_*.csv'))
        icl2_print_file_path = next(self.test_output_directory.glob('P_IC_ICL2_*.csv'))

        with open(processed_sample_file_path) as processed_sample_file:
            processed_sample_file_rows = list(csv.DictReader(processed_sample_file))

        processed_sample_file_rows_england = (row for row in processed_sample_file_rows if
                                              row['TREATMENT_CODE'][-1] == 'E')
        processed_sample_file_rows_wales = (row for row in processed_sample_file_rows if
                                            row['TREATMENT_CODE'][-1] == 'W')

        TestGeneratePrintFile.check_print_file_against_processed_sample_rows(
            icl1_print_file_path, 'P_IC_ICL1', processed_sample_file_rows_england
        )
        TestGeneratePrintFile.check_print_file_against_processed_sample_rows(
            icl2_print_file_path, 'P_IC_ICL2', processed_sample_file_rows_wales
        )

    @staticmethod
    def check_print_file_against_processed_sample_rows(print_file_path, productpack_code, processed_sample_rows):
        fieldnames = ('UAC', 'CASE_REF', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3', 'TOWN_NAME', 'POSTCODE',
                      'PRODUCTPACK_CODE')
        with open(print_file_path) as print_file:

            print_file_reader = csv.DictReader(print_file, fieldnames=fieldnames, delimiter='|')

            for print_row in print_file_reader:
                processed_sample_row = next(processed_sample_rows)
                assert print_row.pop('PRODUCTPACK_CODE') == productpack_code
                for key, value in print_row.items():
                    assert processed_sample_row[key] == value, (f'expected: [{processed_sample_row[key]}] '
                                                                f'but found [{value}] '
                                                                f'for field: [{key}] in file [{print_file_path}]')
