from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("config.env")

# Read values
PROJECT_NAME = os.getenv("PROJECT_NAME")
RAW_PATH = os.getenv("RAW_PATH")
PROCESSED_PATH = os.getenv("PROCESSED_PATH")
REPORTS_PATH = os.getenv("REPORTS_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")
SPARK_APP_NAME = os.getenv("SPARK_APP_NAME")
SPARK_MASTER = os.getenv("SPARK_MASTER")
LOG_LEVEL = os.getenv("LOG_LEVEL")
GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_BUCKET = os.getenv("GCP_BUCKET")
BQ_DATASET = os.getenv("BQ_DATASET")

# Print values
print("PROJECT_NAME :", PROJECT_NAME)
print("RAW_PATH :", RAW_PATH)
print("PROCESSED_PATH :", PROCESSED_PATH)
print("REPORTS_PATH :", REPORTS_PATH)
print("LOGS_PATH :", LOGS_PATH)
print("SPARK_APP_NAME :", SPARK_APP_NAME)
print("SPARK_MASTER :", SPARK_MASTER)
print("LOG_LEVEL :", LOG_LEVEL)
print("GCP_PROJECT :", GCP_PROJECT)
print("GCP_BUCKET :", GCP_BUCKET)
print("BQ_DATASET :", BQ_DATASET)
