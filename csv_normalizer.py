#!/usr/bin/env python3

import argparse
import os
import re


def files_group(path, backup=True):
    regex = re.compile(r'uhtt_barcode_ref_\d{4}\.csv')
    for f in os.listdir(path):
        if regex.match(f):
            main(os.path.join(path, f), backup)


def main(filename, backup=True):
    backup_filename = filename + '.bak'
    os.rename(filename, backup_filename)

    regex = re.compile(r'^\d')
    with open(backup_filename) as read_from, open(filename, 'w', newline='') as write_to:
        ch = 0
        first_line = True
        for line in read_from:
            if line.endswith('\n'):
                line = line[:-1]

            if not line:
                continue

            if regex.match(line):
                write_to.write('\n')
                write_to.write(line)
            else:
                if first_line:
                    first_line = False
                else:
                    ch += 1
                write_to.write(line)

        write_to.write('\n')

        if ch:
            print(filename + ": Changed lines", ch)
    if not backup:
        os.remove(backup_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for normalize barcode list from https://github.com/papyrussolution/UhttBarcodeReference')
    parser.add_argument('-b', '--backup', action='store_true')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-d', '--path', help='Path to dir with csv')
    source.add_argument('-f', '--file', help='Path to release csv file')
    args = parser.parse_args()

    if args.path:
        files_group(args.path, args.backup)
    else:
        main(args.file, args.backup)
