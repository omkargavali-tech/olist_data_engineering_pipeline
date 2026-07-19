#!/usr/bin/env python3

"""
profiler.py
Purpose:
    Profile all raw CSV files before ETL processing.

Output:
    Prints profiling information to the console.
    When run with nohup, the output is saved to logs/profiler.log.
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("raw")


def profile_csv(file_path):
    print("=" * 70)
    print(f"Dataset : {file_path.name}")

    try:
        df = pd.read_csv(file_path)

        print(f"Rows               : {len(df)}")
        print(f"Columns            : {len(df.columns)}")
        print(f"Column Names       : {list(df.columns)}")
        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

        print(f"\nDuplicate Rows     : {df.duplicated().sum()}")

    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")

    print()


def main():
    print("========== OLIST RAW DATA PROFILER ==========\n")

    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in raw/")
        return

    for csv_file in csv_files:
        profile_csv(csv_file)

    print("========== PROFILING COMPLETED ==========")


if __name__ == "__main__":
    main()
