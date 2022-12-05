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

    return int(zigzag_days[dt.weekday()])




if __name__ == "__main__":
    calorie_dict = {}
    max_calories = 0
    calories_in_plan = 0
    try:
        mealplan_path = Path(sys.argv[1])
    except:
        print("Something is wrong with your arguments try again")

    if not mealplan_path.is_file():
        print("Incorrect file path", sys.argv[1])
        exit()
    
    with open("./calorieslist.csv") as calorie_list:
        csv_reader = csv.reader(calorie_list)
        
        for row in csv_reader:
            calorie_dict[row[0]] = int(row[1])/int(row[2])

    with open(mealplan_path) as mealplan_csv:
        csv_reader = csv.reader(mealplan_csv, delimiter=',', skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if len(row) not in (1, 8):
                    print("Your calories line does not meet the correct format.")
                    exit()
                max_calories = extract_calories(row)
                line_count += 1
            else:
                if "#" not in row[0]:
                    calories_in_plan += int(row[1]) * calorie_dict[row[0]]
    
    print("Calories Allowed Today:", int(max_calories))
    print("Calories In Plan:", int(calories_in_plan))
    print("Excess calories: ", int(calories_in_plan - max_calories))
    print("Percentage of calories in plan:", int(calories_in_plan / max_calories * 100))
