#!/usr/bin/env python

'''
Script to convert csv file to YNAB expected format

"Date", "Payee", "Memo", "Outflow", "Inflow"
'''

import argparse
import csv
import re
from pathlib import Path


def get_update_date(input_file):
    re_update_date = re.compile(r"^.*To (\d{2})/(\d{2})/(\d{4})")

    with open(input_file, "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            for column in row:
                str = re_update_date.match(column)
                if str is not None:
                    day = str[1]
                    month = str[2]
                    year = str[3]

    return year, month, day


def process_cc_data(row):
    outflow = 0
    inflow = 0
    if row[2] == "DR":
        outflow = row[3]
    elif row[2] == "CR":
        inflow = row[3]

    return outflow, inflow


def process_bank_data(row):
    outflow = row[4]
    inflow = row[5]

    return outflow, inflow


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse ')
    parser.add_argument('path', type=str, help='Path to the csv file.')

    args = parser.parse_args()

    inpath = Path(args.path)
    year, month, date = get_update_date(inpath)
    outpath = Path(f"output_{inpath.stem}_{year}{month}{date}{inpath.suffix}")

    print(f"Converted data will be stored in: {outpath}")

    if inpath.stem in ["touchpoint", "traveller"]:
        with open(inpath, "r") as infile:
            with open(outpath, "w") as outfile:
                reader = csv.reader(infile)
                writer = csv.DictWriter(
                    outfile, ["Date", "Payee", "Memo", "Inflow", "Outflow"])
                writer.writeheader()

                re_date = re.compile(r"\d{2}/\d{2}/\d{4}")
                for row in reader:
                    for column in row:
                        if re_date.match(column):
                            outflow, inflow = process_cc_data(row)

                            writer.writerow(
                                {"Date": row[0], "Payee": "", "Memo": row[1],
                                 "Inflow": inflow, "Outflow": outflow})
    else:
        with open(inpath, "r") as infile:
            with open(outpath, "w") as outfile:
                reader = csv.reader(infile)
                writer = csv.DictWriter(
                    outfile, ["Date", "Payee", "Memo", "Inflow", "Outflow"])
                writer.writeheader()

                re_date = re.compile(r"\d{2}/\d{2}/\d{4}")
                for row in reader:
                    if re_date.match(row[1]):
                        outflow, inflow = process_bank_data(row)

                        writer.writerow(
                            {"Date": row[1], "Payee": "", "Memo": row[3],
                             "Inflow": inflow, "Outflow": outflow})
