#!/usr/bin/env python

import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse ')
    parser.add_argument('path', type=str, help='Path to the csv file.')

    args = parser.parse_args()

    with open(args.path, "r") as infile:
        with open("./output.csv", "w") as outfile:
            content = csv.reader(infile)

            for row in content:
                print(row)
