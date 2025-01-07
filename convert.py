#!/usr/bin/env python

'''
Script to convert csv file to YNAB expected format

"Date", "Payee", "Memo", "Outflow", "Inflow"
'''

import argparse
import csv
import re
from pathlib import Path

import pandas as pd


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


def process_cc_data_df(row):
    outflow = 0
    inflow = 0
    if row.Dir == "CR":
        inflow = row.Val
    elif row.Dir == "DR":
        outflow = row.Val

    return pd.Series([inflow, outflow])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse ')
    parser.add_argument('path', type=str, help='Path to the csv file.')

    args = parser.parse_args()

    inpath = Path(args.path)
    year, month, date = get_update_date(inpath)
    outpath = Path(f"output_{inpath.stem}_{year}{month}{date}{inpath.suffix}")

    print(f"Converted data will be stored in: {outpath}")

    column_name = ["Date", "Payee", "Memo", "Inflow", "Outflow"]
    if inpath.stem in ["diff_touchpoint", "diff_traveller"]:
        csv_df = pd.read_csv(str(inpath.resolve()),
                             names=["Date", "Memo", "Dir", "Val"],
                             dtype={'Val': str},
                             skiprows=[0])
        df = pd.DataFrame(csv_df, columns=column_name[:3])
        df[column_name[3:]] = csv_df.apply(process_cc_data_df, axis=1)

    else:
        csv_df = pd.read_csv(str(inpath.resolve()),
                             names=["Date", "ValueDate", "Ref", "Memo",
                                    "Outflow", "Inflow", "Balance"],
                             dtype={'Outflow': str, 'Inflow': str},
                             skiprows=[0, 1])
        __import__('ipdb').set_trace()

        df = pd.DataFrame(csv_df, columns=column_name)

    df = df.fillna('')
    # TODO: Convert to the real filename
    df.to_csv("test.csv", index=False)
    print(df)
