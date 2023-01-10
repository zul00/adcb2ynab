#!/usr/bin/env python

'''
Script to convert csv file to YNAB expected format

"Date", "Payee", "Memo", "Outflow", "Inflow"
'''

import argparse
import csv
import re
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse ')
    parser.add_argument('path', type=str, help='Path to the csv file.')

    args = parser.parse_args()

    inpath = Path(args.path)
    outpath = Path("output_" + inpath.name)

    print(f"Converted data will be stored in: {outpath}")

    with open(inpath, "r") as infile:
        with open(outpath, "w") as outfile:
            reader = csv.reader(infile)
            writer = csv.DictWriter(
                outfile, ["Date", "Payee", "Memo", "Inflow", "Outflow"])
            writer.writeheader()

            re_date = re.compile(r"\d{2}/\d{2}/\d{4}")
            for row in reader:
                if re_date.match(row[1]):
                    outflow = row[4]
                    inflow = row[5]

                    writer.writerow(
                        {"Date": row[1], "Payee": "", "Memo": row[3],
                         "Inflow": inflow, "Outflow": outflow})

