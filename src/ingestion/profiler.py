"""
profiler.py

Purpose:
    Profile all Olist raw CSV files, validate schemas,
    generate JSON reports, and log the ingestion process.
"""

import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

from src.utils.logger import get_logger

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv("config.env")

RAW_PATH = os.getenv("RAW_PATH", "./raw")
REPORTS_PATH = os.getenv("REPORTS_PATH", "./reports")

logger = get_logger("profiler")

# --------------------------------------------------
# Expected schemas
# --------------------------------------------------
EXPECTED_SCHEMAS = {
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "payments": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
}


# --------------------------------------------------
# Read CSV safely
# --------------------------------------------------
def safe_read(filepath: str, **kwargs) -> Optional[pd.DataFrame]:
    """
    Safely read a CSV file.

    Returns:
        pandas.DataFrame if successful, otherwise None.
    """
    try:
        df = pd.read_csv(filepath, **kwargs)

        logger.info(
            f"Loaded: {filepath} | "
            f"{df.shape[0]} rows | "
            f"{df.shape[1]} columns"
        )

        return df

    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")

    except pd.errors.EmptyDataError:
        logger.error(f"Empty file: {filepath}")

    except pd.errors.ParserError as err:
        logger.error(f"Parser error in {filepath}: {err}")

    except Exception:
        logger.exception(f"Unexpected error while reading {filepath}")

    return None


# --------------------------------------------------
# Profile DataFrame
# --------------------------------------------------
def profile_dataframe(df: pd.DataFrame, name: str) -> dict:
    """
    Generate profiling statistics for a dataframe.
    """

    null_counts = df.isnull().sum().to_dict()

    null_pct = (
        (df.isnull().sum() / len(df) * 100)
        .round(2)
        .to_dict()
    )

    duplicate_rows = int(df.duplicated().sum())

    profile = {
        "table": name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "null_counts": null_counts,
        "null_pct": null_pct,
        "duplicate_rows": duplicate_rows,
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2,
        ),
    }

    logger.info(
        f"{name}: "
        f"{profile['rows']} rows | "
        f"{duplicate_rows} duplicates | "
        f"{sum(null_counts.values())} null values"
    )

    return profile


# --------------------------------------------------
# Schema Validation
# --------------------------------------------------
def validate_schema(
    df: pd.DataFrame,
    table_name: str,
    expected_columns: list,
) -> bool:
    """
    Validate dataframe schema.
    """

    actual = set(df.columns)
    expected = set(expected_columns)

    missing = expected - actual
    extra = actual - expected

    if missing:
        logger.warning(
            f"{table_name}: Missing columns -> {sorted(missing)}"
        )

    if extra:
        logger.info(
            f"{table_name}: Extra columns -> {sorted(extra)}"
        )

    valid = len(missing) == 0

    logger.info(
        f"{table_name}: Schema validation = {valid}"
    )

    return valid


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    logger.info("=" * 60)
    logger.info("OLIST DATA PROFILER STARTED")
    logger.info("=" * 60)

    files = {
        "orders": "olist_orders_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "customers": "olist_customers_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "payments": "olist_order_payments_dataset.csv",
        "reviews": "olist_order_reviews_dataset.csv",
        "category_translation": "product_category_name_translation.csv",
    }

    all_profiles = {}

    for table_name, filename in files.items():

        filepath = os.path.join(RAW_PATH, filename)

        df = safe_read(
            filepath,
            low_memory=False,
        )

        if df is None:
            logger.error(f"Skipping {table_name}")
            continue

        if df.empty:
            logger.warning(f"{table_name} is empty")
            continue

        profile = profile_dataframe(df, table_name)

        all_profiles[table_name] = profile

        if table_name in EXPECTED_SCHEMAS:
            validate_schema(
                df,
                table_name,
                EXPECTED_SCHEMAS[table_name],
            )

    os.makedirs(REPORTS_PATH, exist_ok=True)

    report_path = os.path.join(
        REPORTS_PATH,
        f"raw_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    )

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(
            all_profiles,
            file,
            indent=4,
            default=str,
        )

    logger.info(f"Profile report saved: {report_path}")
    logger.info("OLIST DATA PROFILER COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()