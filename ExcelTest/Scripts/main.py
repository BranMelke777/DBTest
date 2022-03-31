import json
import sys
import numpy as np
import pandas as pd
import os
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")


class Excels:
    def __init__(self, data):
        self.dt_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.dirPath = r'{}\ExcelOutputs'.format(os.path.dirname(os.path.abspath(__file__)))
        self.excelFilePath = data['excelFile']
        # self.excelFile = pd.read_excel(r"C:\Users\flexn\pythonProject\DBTest\QA_home_assignment_2022.xlsx")
        self.on = [data['sheet2'][1], data['sheet2'][2]]
        self.ssheet1 = self.getDbSheet(self.excelFilePath, data['sheet1'][0], [data['sheet1'][1], data['sheet1'][2]])
        self.ssheet2 = self.getDbSheet(self.excelFilePath, data['sheet2'][0], self.on)
        self.fsheet1 = self.getDbSheet(self.excelFilePath, data['sheet1'][0])
        self.fsheet2 = self.getDbSheet(self.excelFilePath, data['sheet2'][0])
        self.ssheet1.columns = self.on
        self.answers = self.answers()

    # Function: CreateOutputs
    # Description: create new output directory and saves Excel sheets results
    def createOutputs(self):
        try:
            if not os.path.exists(self.dirPath):
                print('Creating output directory...')
                os.makedirs(self.dirPath)
        except OSError as e:
            print("Couldn't create output directory, Error: {}".format(e))
            sys.exit(1)
        try:
            results1 = self.compareExcels(self.ssheet1, self.ssheet2, self.on,
                                          self.fsheet1)
            results2 = self.compareExcels(self.ssheet2, self.ssheet1, self.on,
                                          self.fsheet2)

            with pd.ExcelWriter('{}\{}-Results.xlsx'.format(self.dirPath, self.dt_string)) as writer:
                print('Creating excel results file...')
                results1.to_excel(writer, sheet_name='{}_results'.format(data['sheet1'][0]))
                results2.to_excel(writer, sheet_name='{}_results'.format(data['sheet2'][0]))
                self.answers.to_excel(writer, sheet_name='Answers')
        except Exception as e:
            print("Couldn't create Excel output file, Error: {}".format(e))

    # Function: getDbSheet
    # Description: Read the Excel and
    # params: Excel file, sheet name , columns
    # returns: the full specific sheet or with specific columns
    def getDbSheet(self, file, sheet_name, usecols=None):
        # print('Reading the excel file...')
        if usecols is not None:
            return pd.read_excel(file, sheet_name=sheet_name, usecols=usecols)
        else:
            return pd.read_excel(file, sheet_name=sheet_name)

    # Function: compareExcels
    # Description: compare 2 Excels
    # params: sheet1, sheet2, columns to compare, full sheet1
    # return: A new DataFrame object contains the rows that not exists in the second excel
    def compareExcels(self, sheet1, sheet2, on, full_sheet):
        # print('comparing the two Excels...')
        df = sheet1.merge(sheet2, on=on, how='left', indicator='Exist')
        df['Exist'] = np.where(df.Exist == 'both', True, False)
        newData = pd.DataFrame(columns=list(full_sheet.columns.values))
        for i, row in enumerate(df.values):
            if False in row:
                newData = newData.append(full_sheet.iloc[i])
        return newData

    # Function: answers
    # Description: Check if the number of rows are equal in 2 Excels
    # params: Excel file, sheet name , columns
    # return: A new DataFrame object contains the answers
    def answers(self):
        bol = False
        adjust = []
        sheet1 = len(self.fsheet1.index)
        sheet2 = len(self.fsheet2.index)
        if sheet1 == sheet2:
            bol = True
        if bol is False:
            if sheet1 > sheet2:
                adjust.append('Table:{}'.format(data['sheet2'][0]))
                adjust.append('Add {} rows to adjust the data'.format(sheet1 - sheet2))
            else:
                adjust.append('Table:{}'.format(data['sheet1'][0]))
                adjust.append('Add {} rows to adjust the data'.format(sheet2 - sheet1))
        else:
            adjust.append('No need to adjust')
            adjust.append('The data length is equal in both tablas')
        return pd.DataFrame({"Questions": ['Are the number of rows in Legacy DB the same as Scalable DB?', 'need to '
                                                                                                           'adjust '
                                                                                                           'the data '
                                                                                                           'in one of '
                                                                                                           'the '
                                                                                                           'tables?'],
                             "Answers": ['{}'.format(bol), 'Adjust the data: {} - {}'.format(adjust[0], adjust[1])]})


if __name__ == "__main__":
    if sys.argv[1]:
        with open(sys.argv[1]) as f:
            data = json.load(f)
        obj = Excels(data)
        obj.createOutputs()
