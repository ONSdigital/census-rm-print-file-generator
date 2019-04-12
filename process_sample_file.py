import argparse
import csv
import sys
import uuid
from itertools import tee
from typing import Iterable

from iac_controller import IACController


def process_sample_file_from_path(sample_file_path, output_file_path):
    with open(sample_file_path) as sample_file:
        sample_file, sample_file_line_counter = tee(sample_file)
        sample_size = sum(1 for _ in sample_file_line_counter) - 1
        process_sample_file_rows(sample_file, sample_size, output_file_path)


def process_sample_file_rows(sample_file: Iterable[str], sample_size, output_file_path):
    print(f'Preparing to process {sample_size} sample units')

    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    iac_controller = IACController(max_total_iacs=sample_size)
    fieldnames = sample_file_reader.fieldnames + ['CASE_REF', 'UAC', 'QID']

    with open(output_file_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for count, sample_row in enumerate(sample_file_reader):
            processed_row = process_sample_row(count, iac_controller, sample_row)
            writer.writerow(processed_row)
            if not count % 1000:
                sys.stdout.write(f'\rProcessed {count} sample units')
                sys.stdout.flush()

    print(f'\nAll {sample_size} processed sample units written to {output_file_path}')


def process_sample_row(count: int, iac_controller: IACController, sample_row: dict):
    processed_row = sample_row.copy()
    processed_row.update({
        'CASE_REF': str(count).zfill(12),
        'UAC': iac_controller.get_iac(),
        'QID': uuid.uuid4()
    })
    return processed_row


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process sample file to make it ready for print file generation')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('output_file_path', help='path to write the processed file to', type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()
    process_sample_file_from_path(args.sample_file_path, args.output_file_path)


if __name__ == "__main__":
    main()
