#!/usr/bin/env python

'''
Script to convert csv file to YNAB expected format

"Date", "Payee", "Memo", "Outflow", "Inflow"
'''

import argparse
import csv
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse ')
    parser.add_argument('path', type=str, help='Path to the csv file.')

    args = parser.parse_args()

    with open(args.path, "r") as infile:
        # TODO: Change it to an argument? Or convert it from input
        with open("./output.csv", "w") as outfile:
            reader = csv.reader(infile)
            writer = csv.DictWriter(
                outfile, ["Date", "Payee", "Memo", "Inflow", "Outflow"])
            writer.writeheader()

            re_date = re.compile(r"\d{2}/\d{2}/\d{4}")
            for row in reader:
                for column in row:
                    if re_date.match(column):
                        outflow = 0
                        inflow = 0
                        if row[2] == "DR":
                            outflow = row[3]
                        elif row[2] == "CR":
                            inflow = row[3]

                        writer.writerow(
                            {"Date": row[0], "Payee": "", "Memo": row[1],
                             "Inflow": inflow, "Outflow": outflow})
