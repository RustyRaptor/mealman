#! /bin/python

import sys
from pathlib import Path
import csv

def extract_calories(first_row):
    pass

if __name__ == "__main__":
    max_calories = 0

    mealplan_path = Path(sys.argv[1])

    if not mealplan_path.is_file():
        print("Incorrect file path", sys.argv[1])
        exit()

    with open(mealplan_path) as mealplan_csv:
        csv_reader = csv.reader(mealplan_csv, delimiter=', ')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                max_calories = extract_calories(row)
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
    
    


