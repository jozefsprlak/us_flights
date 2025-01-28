import os
import pandas as pd


def generate_all_combinations(start: tuple[int, int], end: tuple[int, int]) -> pd.DataFrame:
    start_year, start_month = start
    end_year, end_month = end

    all_years = range(start_year, end_year + 1)
    all_months = range(1, 13)

    return pd.DataFrame(
        [(year, month) for year in all_years for month in all_months
         if not (year == start_year and month < start_month) \
         and not (year == end_year and month > end_month)],
        columns=["Year", "Month"]
    )


def identify_missing_combinations(flights_data: pd.DataFrame,
                                  all_combinations: pd.DataFrame) -> pd.DataFrame:
    existing_combinations = flights_data.drop_duplicates(subset=["Year", "Month"])[
        ["Year", "Month"]
    ]

    all_combinations = pd.merge(
        all_combinations, existing_combinations, how="left", indicator=True
    )
    all_combinations = all_combinations[all_combinations["_merge"] == "left_only"]
    return all_combinations.drop(columns="_merge")


def get_missing_combinations(output_csv: str,
                             start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    all_combinations = generate_all_combinations(start, end)
    try:
        if os.path.exists(output_csv):
            flights_data = pd.read_csv(output_csv, low_memory=False)
            all_combinations = identify_missing_combinations(flights_data, all_combinations)
        else:
            print("No existing data found. Assuming all combinations are missing.")

    except Exception as e:
        print(f"Error identifying missing combinations: {e}")

    array = [tuple(row) for row in all_combinations.values]

    return [(int(x), int(y)) for x, y in array]


def combinations_found(output_file_csv: str,
                       start: tuple[int, int],
                       end: tuple[int, int]) -> list[tuple[int, int]]:
    missing_combinations = get_missing_combinations(output_file_csv, start, end)

    if len(missing_combinations) > 0:
        print(f"Missing combinations found. Processing {len(missing_combinations)} files...")
    else:
        print("No missing combinations to process.")
    return missing_combinations
