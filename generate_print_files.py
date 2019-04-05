import argparse
import csv
import os
from contextlib import ExitStack
from datetime import datetime
from itertools import tee
from typing import Iterable


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('output_file_path', help='path to write the print file', type=str)
    return parser.parse_args()


def load_sample_file(sample_file_path, output_file_location):
    with open(sample_file_path) as sample_file:
        load_sample(sample_file, output_file_location)


def load_sample(sample_file: Iterable[str], output_file_location):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    sample_file_reader, copy_sample_file_reader = tee(sample_file_reader)
    sample_size = sum(1 for _ in copy_sample_file_reader)
    print(f'Preparing to process {sample_size} sample units')

    _generate_print_files(sample_file_reader, output_file_location, sample_size)


def _generate_print_files(sample_file_reader, output_file_location, sample_size):
    print_file_productpack_codes = ['P_IC_ICL1', 'P_IC_ICL2']
    with ExitStack() as stack:
        print_files = {
            productpack_code: stack.enter_context(
                open(os.path.join(output_file_location, f'{productpack_code}_{datetime.utcnow().strftime("%Y-%M-%dT%H-%M-%S")}.csv'), 'w'))
            for productpack_code in print_file_productpack_codes}
        field_names = ('uac', 'caseref', 'address_line1', 'address_line2', 'address_line3', 'town_name', 'postcode', 'productpack_code')
        csv_writers = {productpack_code: csv.DictWriter(print_file, fieldnames=field_names, delimiter='|')
                       for productpack_code, print_file in print_files.items()}

        for count, sample_row in enumerate(sample_file_reader):
            row = {
                'uac': sample_row['UAC'],
                'caseref': sample_row['CASE_REF'],
                'address_line1': sample_row['ADDRESS_LINE1'],
                'address_line2': sample_row['ADDRESS_LINE2'],
                'address_line3': sample_row['ADDRESS_LINE3'],
                'town_name': sample_row['TOWN_NAME'],
                'postcode': sample_row['POSTCODE'],
            }
            productpack_code = get_productpack_code_for_treatment_code(sample_row['TREATMENT_CODE'])
            row['productpack_code'] = productpack_code
            csv_writers[productpack_code].writerow(row)

            if count % (sample_size // 10) == 0:
                print(f'Processed {count} sample units')
    print('Finished')


def get_productpack_code_for_treatment_code(treatment_code: str) -> str:
    return {
        'E': 'P_IC_ICL1',
        'W': 'P_IC_ICL2'
    }.get(treatment_code[-1])


def main():
    args = parse_arguments()
    load_sample_file(args.sample_file_path, args.output_file_path)


if __name__ == "__main__":
    main()
