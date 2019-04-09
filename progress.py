import sys


def print_sample_units_progress(number_processed, total):
    if total // 100:
        if not number_processed % (total // 100):
            sys.stdout.write(f'\rProcessed {number_processed} sample units')
            sys.stdout.flush()
        if number_processed >= total:
            print()
