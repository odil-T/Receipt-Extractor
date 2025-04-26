# Receipt Extractor

import re
import pandas as pd
from PIL import Image
import pytesseract


original_image = 'images/receipt.webp'

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\o.tohirov\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
raw_text = pytesseract.image_to_string(Image.open(original_image), lang="eng+rus")

match_date = re.search(r"\d{2}\.\d{2}\.\d{4}", raw_text)
match_total = re.search(r"(?<=оБщий ).*", raw_text, re.IGNORECASE)
match_location = re.search(r"г\..+", raw_text)

date = match_date.group() if match_date else None
total = match_total.group() if match_total else None
location = match_location.group() if match_location else None

item_info_pattern = re.compile(r"[*=]|\d+шт")

for line in raw_text.splitlines():
    if item_info_pattern.search(line):
        match_item_name = re.search(r"^[A-Za-zА-Яа-яёЁ\s']*(?=[^A-Za-zА-Яа-яёЁ']|$)", line)
        match_item_quantity = re.search(r"[\d.]+(?=\*)", line)
        match_item_price = re.search(r"(?<=\*)[\d,.]+(?=[^\d,.]|$)", line)

        item_name = match_item_name.group().strip() if match_item_name else None
        item_quantity = match_item_quantity.group().strip() if match_item_quantity else None
        item_price = match_item_price.group().replace(",", "") if match_item_price else None

