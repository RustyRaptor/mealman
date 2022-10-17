#! /bin/python

import sys
from pathlib import Path
import csv
from datetime import datetime

def extract_calories(first_row):
    if first_row[0] != "zigzag":
        return int(first_row[0])
    dt = datetime.now()
    zigzag_days = first_row[1:]

    return zigzag_days[dt.weekday()]




if __name__ == "__main__":
    max_calories = 0

    mealplan_path = Path(sys.argv[1])

    if not mealplan_path.is_file():
        print("Incorrect file path", sys.argv[1])
        exit()

    with open(mealplan_path) as mealplan_csv:
        csv_reader = csv.reader(mealplan_csv, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                max_calories = extract_calories(row)
                line_count += 1
            else:
                print(row)
    
    


