import pandas as pd
import numpy as np
import openpyxl
import os
import datetime


FILES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', 'staticfiles', 'excel', 'xlsx'))


ALL_FILES = [
    '/Users/touchdara/Documents/GitHub/kam12project/backend/staticfiles/excel/xlsx/KAM12_MonthlyReport_Jan_2024.xlsx',
    '/Users/touchdara/Documents/GitHub/kam12project/backend/staticfiles/excel/xlsx/KAM12_MonthlyReport_Jan_2024_1.xlsx',
    os.path.join(FILES_PATH, 'KAM12_MonthlyReport_Feb_2024.xlsx'),
    # os.path.join(FILES_PATH, 'KAM12_MonthlyReport_Mar_2024.xlsx'),
    os.path.join(FILES_PATH, 'KAM12_MonthlyReport_Mar_2024 copy.xlsx'),
    # '/Users/touchdara/Documents/GitHub/kam12project/backend/temp/budget.xlsx',
    ]


class Salakabatt:
    """
        - Read the individual excel file
    """

    def __init__(self, file_path, *args, **kwargs):
        self.workbook = pd.ExcelFile(file_path, engine='openpyxl')

    def tax_data(self):
        """
            - Read the first sheet of the excel file (សារពើពន្ធ​)
            - Return: Data from the first sheet of the excel file
        """
        tax_df = self.workbook.parse(
            sheet_name=self.workbook.sheet_names[0],
            na_filter=False,
            dtype=object,
            header=None,
            )
        tax_df.iloc[:, 2] = pd.to_datetime(
            tax_df.iloc[:, 2],
            dayfirst=True,
            format='%d/%m/%Y',
            errors='coerce'
            )
        tax_df.iloc[:, 3:19] = tax_df.iloc[:, 3:19].apply(
            pd.to_numeric,
            errors='coerce'
            )
        tax_df = tax_df[tax_df.iloc[:, 2].notnull()]

        return tax_df


    def non_tax_data(self):
        """
            - Read the second sheet of the excel file (មិនមែនសារពើពន្ធ​)
            - Return: Data from the second sheet of the excel file
        """

        non_tax_df = self.workbook.parse(
            sheet_name=self.workbook.sheet_names[1],
            na_filter=False,
            dtype=object,
            header=None, 
        )
        non_tax_df.iloc[:,2] = pd.to_datetime(
            non_tax_df.iloc[:, 2],
            dayfirst=True,
            format='%d/%m/%Y',
            errors='coerce'
        )
        non_tax_df.iloc[:, 3:19] = non_tax_df.iloc[:, 3:19].apply(
            pd.to_numeric,
            errors='coerce'
        )
        non_tax_df = non_tax_df[non_tax_df.iloc[:, 2].notnull()]

        return non_tax_df


class AllSalakabatt:
    """
        - Read all the excel files
    """
    def __init__(self, list_of_file_path: list, *args, **kwargs):
        self.files = list_of_file_path
        self.tax_data = self.__all_tax_data()
        self.non_tax_data = self.__all_non_tax_data()

    def __all_tax_data(self):
        tax_data_list = []
        for file in self.files:
            tax_data = Salakabatt(file).tax_data()
            tax_data_list.append(tax_data)
        
        combined_tax_data = pd.concat(tax_data_list, ignore_index=True)
        
        return combined_tax_data

    def __all_non_tax_data(self):
        non_tax_data_list = []
        for file in self.files:
            non_tax_data = Salakabatt(file).non_tax_data()
            non_tax_data_list.append(non_tax_data)
        combined_non_tax_data = pd.concat(non_tax_data_list, ignore_index=True)
        
        return combined_non_tax_data

    def income_by_date(self, date_val: datetime.datetime, income_code: str):
        """
             - Return income on a specific date
        """
        TAX_INCOME_CODE_MAP = {
            'VPP': 4, # 70025
            'VOP': 5, # 70026
            'SPP': 6, # 70032
            'SOP': 7, # 70033
            'COP': 8, # 71001

            'CPP': 10, # 71003
            'ATP': 11, # 71004
            'AUC': 12, # 71005
            'PIM': 13, # 71006
            'ETW': 14, # 71011
            'ETR': 15, # 71012
            'ETP': 16, # 71013
            'ETO': 17, # 71014
            'PEX': 18, # 71016
        }
        NON_TAX_INCOME_CODE_MAP = {
            'SOS': 4, # 73011
            '73012': 5, # 73012
            'SOM': 6, # 73013
            'SOV': 7, # 73015
            'SOD': 8, # 73016
            'SOE': 9, # 73017
            'SOO': 10, # 73018
            'CBF': 11, # 73024
            '73028': 12, # 73028
            '73048': 13, # 73048
            '73066': 14, # 73066
            'ROL': 15, # 73071
            'ROB': 16, # 73072
            'ROO': 17, # 73073
            '73087': 18, # 73087
            'ORB': 19, # 76981
        }

        combined_income_code = {**TAX_INCOME_CODE_MAP, **NON_TAX_INCOME_CODE_MAP}

        if income_code.upper() not in combined_income_code:
            return 0

        if not isinstance(date_val, datetime.date):
            raise ValueError(f'Invalid date: {date_val}')

        # Tax Data
        if income_code.upper() in TAX_INCOME_CODE_MAP:
            COLUMN_INDEX = TAX_INCOME_CODE_MAP.get(income_code.upper())
            data = self.tax_data
        # Non-Tax Data
        if income_code.upper() in NON_TAX_INCOME_CODE_MAP:
            COLUMN_INDEX = NON_TAX_INCOME_CODE_MAP.get(income_code.upper())
            data = self.non_tax_data

        income_by_date = data[data.iloc[:, 2] == date_val].iloc[:, COLUMN_INDEX].sum()
        
        return income_by_date

# dara = AllSalakabatt(ALL_FILES)
# val = dara.income_by_date(date_val=datetime.datetime(2024, 2, 12), income_code='VoPss')
# print(val)