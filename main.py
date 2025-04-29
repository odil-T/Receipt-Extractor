"""
Receipt Extractor

Specify the following variables:
1. RECEIPT_FOLDER_PATH - Path to the folder containing the receipt images that must be processed.
2. EXCEL_PATH - Path to the excel workbook where the processed data should be stored. Create this file manually if it does not exist.
3. TESSERACT_PATH - Path to Tesseract OCR executable.

TODO:
- function docs
"""

import os
import pandas as pd
import pytesseract

from utils import parse_receipts, append_data_to_excel


RECEIPT_FOLDER_PATH = "receipts"
EXCEL_PATH = "analytics.xlsx"
TESSERACT_PATH = r"C:\Users\o.tohirov\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

if __name__ == "__main__":
    assert os.path.exists(EXCEL_PATH), f"File {EXCEL_PATH} does not exist. Please create this file manually."

    item_data_dict = parse_receipts(RECEIPT_FOLDER_PATH)
    df = pd.DataFrame(item_data_dict)
    append_data_to_excel(EXCEL_PATH, df)
