import os
import subprocess
import uuid
import pandas as pd


def process_monthly_data_r(file_path: str, r_script_path: str) -> str | None:
    unique_id = uuid.uuid4().hex
    temp_output = f"temp_daily_flight_counts_{unique_id}.csv"

    try:
        result = subprocess.run(
            ["Rscript", r_script_path, file_path, temp_output],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    except Exception as e:
        print(f"Failed to process {file_path} using R script: {e}")
        return None

    if result.returncode == 0:
        return temp_output

    print(f"R script error:\n{result.stderr}")
    return None


def append_data(file_path: str, temp_output: str, output_csv: str) -> None:
    if os.path.exists(output_csv):
        temp_df = pd.read_csv(temp_output, low_memory=False)
        temp_df.to_csv(output_csv, mode='a', index=False, header=False)
        os.remove(temp_output)
    else:
        # File didn't exist before
        os.rename(temp_output, output_csv)

    print(f"Processed and updated: {file_path}")
