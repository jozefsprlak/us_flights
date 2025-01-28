import os
import shutil
import zipfile
from datetime import datetime


def delete_folder(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")

    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and all its contents have been removed.")
    except Exception as e:
        print(f"An error occurred: {e}")


def extract(file_name: str, dest_path: str) -> str:
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    unique_extract_dir = f"extracted/{file_name.split('.')[0]}_{suffix}"

    try:
        os.makedirs(unique_extract_dir, exist_ok=True)
        with zipfile.ZipFile(dest_path, 'r') as zip_ref:
            zip_ref.extractall(unique_extract_dir)

    except Exception as e:
        print(f"Error extracting {file_name}: {e}")

    print(f"Extracted: {file_name}")
    os.remove(dest_path)

    return unique_extract_dir
