import os
import openpyxl
import warnings

__file_path = os.path.abspath(__file__)
stamp_file_path = os.path.abspath(os.path.join(__file_path, "..", "..", "..", 'static', 'excel', 'acc_report.xlsx'))

warnings.filterwarnings("ignore")
