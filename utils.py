import os
import re
import shutil
import pandas as pd
import pytesseract

from PIL import Image
from typing import Dict, Union


def parse_receipts(receipts_folder_path: str) -> Union[Dict, None]:
    """
    Parses images of receipts from the provided folder path. Uses Tesseract OCR and RegEx to extract the product name,
    quantity of product, unit price of product, location, and date given on the receipt. Stores the results as a dictionary
    where one row represents one product.

    Args:
        receipts_folder_path: Path to the folder containing the images of receipts to be parsed.

    Returns:
        dict: A dictionary with keys "Product Name", "Quantity", "Unit Price", "Location", "Date" that have lists as values
        that store the product data.
    """

    def _parse_receipt(image_path: str, item_data_dict: Dict) -> None:
        """
        A helper function to parse a single receipt. Updates the item_data_dict dictionary with the parsed data.

        Args:
            image_path: Path to the image of a receipt to be parsed.
            item_data_dict: A dictionary with keys "Product Name", "Quantity", "Unit Price", "Location", "Date" that have lists as values
        that store the product data.

        Returns:
            None
        """
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
    """
    Appends the data from a dataframe to the specified Excel file.

    Args:
        excel_path: Path to Excel file to append data to.
        output_df: The dataframe that must be appended.

    Returns:
        None
    """
    if output_df.empty:
        print(f"No changes were made to file {excel_path}.")
        return

    output_df.insert(0, "No.", range(1, len(output_df) + 1))
    existing_df = pd.read_excel(excel_path)

    if not existing_df.empty:
        last_no = existing_df["No."].iloc[-1]
        output_df["No."] += last_no
        output_df = pd.concat([existing_df, output_df])

        # Backing up the original Excel file just in case
        backup_path = f'{excel_path[:-5]}_backup.xlsx'
        shutil.copy2(excel_path, backup_path)
        print(f"Backup of file {excel_path} was created at {backup_path}.")

    output_df.to_excel(excel_path, index=False)

    print(f"File {excel_path} has been updated.")