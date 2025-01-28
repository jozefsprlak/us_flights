import os
from concurrent.futures import ThreadPoolExecutor

from data_processing import process_monthly_data_r, append_data
from downloading import download
from file_manager import extract, delete_folder
from missing_combinations import combinations_found


def entire_process(missing_combinations: list[tuple[int, int]],
                   base_url: str,
                   download_dir: str,
                   output_file: str,
                   r_script_path: str,
                   max_workers=4) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for row in missing_combinations:
            print("Processing: ", row)
            executor.submit(one_file, row, base_url,
                            download_dir, output_file, r_script_path)


def run(base_url: str,
        download_dir: str,
        output_file: str,
        r_script_path: str,
        start: tuple[int, int],
        end: tuple[int, int]) -> None:
    missing_combinations = combinations_found(output_file, start, end)
    os.makedirs(download_dir, exist_ok=True)

    while len(missing_combinations) > 0:
        entire_process(missing_combinations, base_url,
                       download_dir, output_file, r_script_path)
        missing_combinations = combinations_found(output_file, start, end)

    print(f"All data processed. Daily flight counts saved to {output_file}")

    delete_folder(download_dir)

def one_file(row: tuple[int, int],
             base_url: str,
             download_dir: str,
             output_file: str,
             r_script_path: str) -> None:
    file_name, dest_path = download(row, base_url, download_dir)
    if file_name is None or dest_path is None:
        return
    unique_extract_dir = extract(file_name, dest_path)

    csv_files = [
        os.path.join(unique_extract_dir, f)
        for f in os.listdir(unique_extract_dir) if f.endswith(".csv")
    ]

    for csv_file in csv_files:
        temp_output = process_monthly_data_r(csv_file, r_script_path)
        if os.path.exists(temp_output):
            append_data(csv_file, temp_output, output_file)

    delete_folder(unique_extract_dir)

    print(f"Cleaned up files for: {file_name}")
