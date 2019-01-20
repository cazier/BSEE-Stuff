#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


import csv


def load_dat(filename: str) -> list:
    """
    Loads the contents of the DAT data file into a list with each line of the file
    into an element of the list.
    """
    with open(file = f'{filename}.dat', mode = u'r') as dat_file:
        return dat_file.read().split(u'\n')


def parse_dat_data(entry: str) -> list:
    """
    Converts a character-width delimitted file into a list.
    Each element in the list is separated per the character length specified in the
    headers file.
    """
    return [
        entry[0:7],
        entry[7:13],
        entry[13:19],
        entry[19:21],
        entry[21],
        entry[22:31],
        entry[31:40],
        entry[40:49],
        entry[49:61],
        entry[61:63],
        entry[63:65],
        entry[65:71],
        entry[71:73],
        entry[73:79],
        entry[79:84],
        entry[84:129],
        entry[129:137],
        entry[137:146],
        entry[146:149],
        entry[149:158],
        entry[158:]]


def make_csv(data: dict) -> None:
    """
    Creates one or more CSV files based off of all of the data. A different file is
    made for each of the years in the data dictionary.
    """
    for year in data.keys():
        with open(file = f'output/{year}.csv', mode = u'w') as csvfile:
            csvwriter = csv.writer(csvfile, dialect=u'excel')
            for row in data[year]:
                csvwriter.writerow(row)


def year_split(year: str, threshold: str) -> str:
    """
    Returns the filename for each CSV file, rounded down to the nearest multiple of
    five, based off of the threshold value set.

    i.e., 1947 -> 1947, 1948 -> 1947, 1953 -> 1952

    The threshold number will provide the baseline used. 1947, 1968, 1989, or 2010
    """
    year: int = int(year)
    threshold: int = int(threshold)

    return str((((year - threshold) // 5) * 5) + threshold)


YEARS: list = ['1947', '1968', '1989', '2010']

if __name__ == '__main__':
    for year in YEARS:
        print(f'Reformatting the data in {year}.dat')

        csv_data: dict = dict()

        data: list = load_dat(filename = year)

        for entry in data:
            converted_entry: list = parse_dat_data(entry = entry)
            split: str = year_split(year = converted_entry[2][:4], threshold = year)

            try:
                csv_data[split].append(converted_entry)

            except KeyError:
                csv_data[split] = [converted_entry]

        make_csv(data = csv_data)
