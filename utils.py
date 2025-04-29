import os
import re
import pandas as pd
import pytesseract

from PIL import Image
from typing import Dict, Union


def parse_receipts(receipts_folder_path: str) -> Union[Dict, None]:
    """"""

    def _parse_receipt(image_path: str, item_data_dict: Dict) -> None:
        print(f"Parsing receipt: {image_path}")

        raw_text = pytesseract.image_to_string(Image.open(image_path), lang="eng+rus")

        match_date = re.search(r"\d{2}\.\d{2}\.\d{4}", raw_text)
        match_location = re.search(r"г\..+", raw_text)
        item_info_pattern = re.compile(r"[*=]|\d+шт")

        date = match_date.group() if match_date else None
        location = match_location.group() if match_location else None

        for line in raw_text.splitlines():
            if item_info_pattern.search(line):
                match_item_name = re.search(r"^[A-Za-zА-Яа-яёЁ\s']*(?=[^A-Za-zА-Яа-яёЁ']|$)", line)
                match_item_quantity = re.search(r"[\d.]+(?=\*)", line)
                match_item_price = re.search(r"(?<=\*)[\d,.]+(?=[^\d,.]|$)", line)

                item_name = match_item_name.group().strip() if match_item_name else None
                item_quantity = match_item_quantity.group().strip() if match_item_quantity else None
                item_price = match_item_price.group().replace(",", "") if match_item_price else None

                item_data_dict["Product Name"].append(item_name)
                item_data_dict["Quantity"].append(item_quantity)
                item_data_dict["Unit Price"].append(item_price)
                item_data_dict["Location"].append(location)
                item_data_dict["Date"].append(date)


    if not bool(os.listdir(receipts_folder_path)):
        print("No receipts were found.")
        return None

    item_data_dict = {k: [] for k in ["Product Name", "Quantity", "Unit Price", "Location", "Date"]}

    for image_name in os.listdir(receipts_folder_path):
        image_path = os.path.join(receipts_folder_path, image_name)
        _parse_receipt(image_path, item_data_dict)

    print("All receipts have been parsed.")
    return item_data_dict


def append_data_to_excel(excel_path: str, output_df: pd.DataFrame) -> None:
    if output_df.empty:
        print("No changes were made.")
        return

    output_df.insert(0, "No.", range(1, len(output_df) + 1))
    existing_df = pd.read_excel(excel_path)

    if not existing_df.empty:
        last_no = existing_df["No."].iloc[-1]
        output_df["No."] += last_no
        output_df = pd.concat([existing_df, output_df])

    output_df.to_excel(excel_path, index=False)

    print(f"File {excel_path} has been updated.")