import sys


def print_sample_units_progress(number_processed, total):
    if number_processed % (total // 10) == 0:
        sys.stdout.write(f'\rProcessed {number_processed} sample units')
        sys.stdout.flush()
    if number_processed >= total:
        print()
