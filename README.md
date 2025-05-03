# Receipt Extractor

## Introduction

A tool for extracting data from images of receipts and saving them in an Excel file. The following data are parsed:
- Product Name
- Product Quantity
- Unit Price
- Location
- Date


## How to Install

#### Prerequisites:
1. Tesseract OCR
2. Python (and pip)

You can install this package using pip. Just run `pip install receipt-extractor`.


## How to Use

#### First-Time Setup:
1. Create an Excel file called `analytics.xlsx`. Extracted data will be stored here.
2. Create a folder called `receipts`. We will use this to store images of our receipts.
3. Specify the path to your Tesseract OCR program using [TODO]. For example [TODO] `C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`.

#### Continous Use:
1. Take clear photos of your receipts and store the images in the `receipts` folder.
2. Open a shell instance in the folder where your Excel file and `receipts` folder are located. 
3. Run the app with `receipt` [TODO]

NOTE: Make sure that your Excel file is closed before running the script or else a `Permission denied` error will appear.



TODO:
- prevent .to_excel method from changing formatting of excel file (even if it is empty)
- https://packaging.python.org/en/latest/tutorials/packaging-projects/
- make a pip package
- add entry point for terminal for command `receipt`
- finish README
- write github tag version 1.0.0
- consider upgrading this app with a VLM for parsing (either local or some free API)