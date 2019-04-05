import argparse
import csv
import uuid
from itertools import tee
from typing import Iterable

from iac_controller import IACController


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('output_file_path', help='path to write the print file', type=str)
    return parser.parse_args()


def load_sample_file(sample_file_path, output_file_path):
    with open(sample_file_path) as sample_file:
        load_sample(sample_file, output_file_path)


def load_sample(sample_file: Iterable[str], output_file_path):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    fieldnames = sample_file_reader.fieldnames
    sample_file_reader, copy_sample_file_reader = tee(sample_file_reader)
    sample_size = sum(1 for _ in copy_sample_file_reader)
    print(f'Preparing to process {sample_size} sample units')

    _process_sample_file(sample_file_reader, output_file_path, sample_size, fieldnames)


def _process_sample_file(sample_file_reader, output_file_path, sample_size, fieldnames):
    iac_controller = IACController(max_total_iacs=sample_size)
    fieldnames.extend(['UAC', 'CASE_REF', 'QID'])
    with open(output_file_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for count, sample_row in enumerate(sample_file_reader):
            row = sample_row
            row.update({
                'UAC': iac_controller.get_iac(),
                'CASE_REF': str(count).zfill(12),
                'QID': uuid.uuid4()
            })
            writer.writerow(row)

            if count % (sample_size // 10) == 0:
                print(f'Processed {count} sample units')
    print('Finished')


def main():
    args = parse_arguments()
    load_sample_file(args.sample_file_path, args.output_file_path)


if __name__ == "__main__":
    main()
