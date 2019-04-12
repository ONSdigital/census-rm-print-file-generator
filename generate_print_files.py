import argparse
import csv
import os
import sys
from contextlib import ExitStack
from datetime import datetime
from itertools import tee
from typing import Iterable

TREATMENT_COUNTRY_TO_PRODUCTPACK_CODE = {
    'E': 'P_IC_ICL1',
    'W': 'P_IC_ICL2'
}


def generate_print_files_from_sample_file_path(sample_file_path: str, output_file_location: str):
    with open(sample_file_path) as sample_file:
        sample_file, sample_file_line_counter = tee(sample_file)
        sample_size = sum(1 for _ in sample_file_line_counter) - 1
        generate_print_files(sample_file, sample_size, output_file_location)


def generate_print_files(sample_file: Iterable[str], sample_size: int, output_file_location: str):
    print(f'Preparing to generate print files for {sample_size} sample units')
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    productpack_codes = TREATMENT_COUNTRY_TO_PRODUCTPACK_CODE.values()
    with ExitStack() as stack:
        print_files = {
            productpack_code: stack.enter_context(
                open(os.path.join(output_file_location,
                                  f'{productpack_code}_{datetime.utcnow().strftime("%Y-%M-%dT%H-%M-%S")}.csv'), 'w'))
            for productpack_code in productpack_codes}
        fieldnames = ('UAC', 'CASE_REF', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3', 'TOWN_NAME', 'POSTCODE',
                      'PRODUCTPACK_CODE')
        csv_writers = {productpack_code: csv.DictWriter(print_file, fieldnames=fieldnames, delimiter='|')
                       for productpack_code, print_file in print_files.items()}

        for count, sample_row in enumerate(sample_file_reader):
            productpack_code = get_productpack_code_for_treatment_code(sample_row['TREATMENT_CODE'])
            csv_writers[productpack_code].writerow(create_print_file_row(productpack_code, sample_row, fieldnames))
            if not count % 1000:
                sys.stdout.write(f'\rProcessed {count} sample units')
                sys.stdout.flush()

    print(f'\nFinished writing {len(print_files)} print file(s): {[file.name for file in print_files.values()]}')


def create_print_file_row(productpack_code: str, sample_row: dict, fieldnames: Iterable[str]) -> dict:
    print_file_row = {field: sample_row.get(field) for field in fieldnames}
    print_file_row['PRODUCTPACK_CODE'] = productpack_code
    return print_file_row


def get_productpack_code_for_treatment_code(treatment_code: str) -> str:
    return TREATMENT_COUNTRY_TO_PRODUCTPACK_CODE.get(treatment_code[-1])


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate initial contact print files from processed sample file')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('output_file_path', help='path to the directory to write the print files to', type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()
    generate_print_files_from_sample_file_path(args.sample_file_path, args.output_file_path)


if __name__ == "__main__":
    main()
