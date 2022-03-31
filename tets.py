import numpy as np
import pandas as pd
import os
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
# create new output directory to save the results
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
dirPath = r'{}\ExcelOutputs'.format(os.path.dirname(os.path.abspath(__file__)))
try:
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
except OSError as e:
    print("Couldn't create output directory, Error: {}".format(e))


# Function: getDbSheet
# Description: Read the Excel and returns the full specific sheet or with specific columns
# params: Excel file, sheet name , columns
def getDbSheet(file, sheet_name, usecols=None):
    if usecols is not None:
        return pd.read_excel(file, sheet_name=sheet_name, usecols=usecols)
    else:
        return pd.read_excel(file, sheet_name=sheet_name)


# Function: compareExcels
# Description: compare Excels and returns a new DataFrame object
# params: sheet1, sheet2, columns to compare, full sheet1
def compareExcels(sheet1, sheet2, on, full_sheet):
    df = sheet1.merge(sheet2, on=on, how='left', indicator='Exist')
    df['Exist'] = np.where(df.Exist == 'both', True, False)
    newData = pd.DataFrame(columns=list(full_sheet.columns.values))
    for i, row in enumerate(df.values):
        if False in row:
            newData = newData.append(full_sheet.iloc[i])
    return newData


# Assign the Excel data to a variable
excelFile = pd.read_excel(r"C:\Users\flexn\pythonProject\DBTest\QA_home_assignment_2022.xlsx")
g = r"C:\Users\flexn\pythonProject\DBTest\QA_home_assignment_2022.xlsx"
# Assign the Excel sheets to a variables
small_Legacy_DB_sheet = getDbSheet(g, 'Legacy DB', ["Brand Action Date", "User Unique ID"])
small_Scalable_DB_sheet = getDbSheet(g, 'Scalable DB', ["Period", "ACID"])
full_Legacy_DB_sheet = getDbSheet(g, 'Legacy DB')
full_Scalable_DB_sheet = getDbSheet(g, 'Scalable DB')
small_Legacy_DB_sheet.columns = ['Period', 'ACID']


# Check if the number of rows is equal and print the answer
bol = False
if len(full_Legacy_DB_sheet.index) == len(full_Scalable_DB_sheet.index):
    bol = True

answers = pd.DataFrame({"Questions": ['Are the number of rows in Legacy DB the same as Scalable DB?'],
                        "Answers": ['{}'.format(bol)]})

on = ["Period", "ACID"]
Legacy_DB_results = compareExcels(small_Legacy_DB_sheet, small_Scalable_DB_sheet, on, full_Legacy_DB_sheet)
Scalable_DB_results = compareExcels(small_Scalable_DB_sheet, small_Legacy_DB_sheet, on, full_Scalable_DB_sheet)

with pd.ExcelWriter('{}\{}-Results.xlsx'.format(dirPath, dt_string)) as writer:
    Legacy_DB_results.to_excel(writer, sheet_name='Legacy_DB_results')
    Scalable_DB_results.to_excel(writer, sheet_name='Scalable_DB_results')
    answers.to_excel(writer, sheet_name='Answers')

