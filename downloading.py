import os
from pysmartdl2 import SmartDL


def download(
        task: tuple[int, int],
        base_url: str,
        download_dir: str) -> tuple[str | None, str | None]:
    year, month = task
    file_name = \
        (f"On_Time_Reporting_Carrier_On_Time_Performance_1987_pres"
         f"ent_{year}_{month}.zip")
    file_url = f"{base_url}{file_name}"
    dest_path = os.path.join(download_dir, file_name)

    try:
        obj = SmartDL(file_url, dest_path, timeout=20, verify=False)
        obj.start()

        if obj.isSuccessful():
            print("Download completed:", obj.get_dest())
            return file_name, dest_path

        print(f"Download failed: {file_name}")
        for error in obj.get_errors():
            print("Error:", error)
        return None, None

    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
        return None, None
