import argparse
import csv
import os
from contextlib import ExitStack
from datetime import datetime
from itertools import tee
from typing import Iterable

from progress import print_sample_units_progress

TREATMENT_CODE_TO_PRODUCTPACK_CODE = {
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
    productpack_codes = TREATMENT_CODE_TO_PRODUCTPACK_CODE.values()
    with ExitStack() as stack:
        print_files = {
            productpack_code: stack.enter_context(
                open(os.path.join(output_file_location,
                                  f'{productpack_code}_{datetime.utcnow().strftime("%Y-%M-%dT%H-%M-%S")}.csv'), 'w'))
            for productpack_code in productpack_codes}
        field_names = ('uac', 'caseref', 'address_line1', 'address_line2', 'address_line3', 'town_name', 'postcode',
                       'productpack_code')
        csv_writers = {productpack_code: csv.DictWriter(print_file, fieldnames=field_names, delimiter='|')
                       for productpack_code, print_file in print_files.items()}

        for count, sample_row in enumerate(sample_file_reader):
            productpack_code = get_productpack_code_for_treatment_code(sample_row['TREATMENT_CODE'])
            csv_writers[productpack_code].writerow(create_print_file_row(productpack_code, sample_row))
            print_sample_units_progress(number_processed=count + 1, total=sample_size)

    print(f'Finished writing {len(print_files)} print file(s): {[file.name for file in print_files.values()]}')


def create_print_file_row(productpack_code: str, sample_row: dict) -> dict:
    return {'uac': sample_row['UAC'],
            'caseref': sample_row['CASE_REF'],
            'address_line1': sample_row['ADDRESS_LINE1'],
            'address_line2': sample_row['ADDRESS_LINE2'],
            'address_line3': sample_row['ADDRESS_LINE3'],
            'town_name': sample_row['TOWN_NAME'],
            'postcode': sample_row['POSTCODE'],
            'productpack_code': productpack_code}


def get_productpack_code_for_treatment_code(treatment_code: str) -> str:
    return TREATMENT_CODE_TO_PRODUCTPACK_CODE.get(treatment_code[-1])


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
