#!/bin/bash

# ============================================
# Script Name : profile_raw_data.sh
# Purpose     : Profile all raw CSV datasets
# Project     : Olist Data Engineering Pipeline
# Author      : Omkar Balaji Gavali
# ============================================

# Exit immediately if any command fails
set -euo pipefail

# --------------------------------------------
# Get project root directory
# --------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

RAW_DIR="$PROJECT_ROOT/raw"
LOG_DIR="$PROJECT_ROOT/logs"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT="$LOG_DIR/raw_profile_$TIMESTAMP.txt"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo "========================================" | tee "$REPORT"
echo "         RAW DATA PROFILE REPORT         " | tee -a "$REPORT"
echo "Generated : $(date)"                    | tee -a "$REPORT"
echo "========================================" | tee -a "$REPORT"

# Check if CSV files exist
if ! ls "$RAW_DIR"/*.csv >/dev/null 2>&1; then
    echo "ERROR: No CSV files found in $RAW_DIR" | tee -a "$REPORT"
    exit 1
fi

# Loop through each CSV file
for file in "$RAW_DIR"/*.csv
do
    filename=$(basename "$file")

    echo "" | tee -a "$REPORT"
    echo "----------------------------------------" | tee -a "$REPORT"
    echo "File Name      : $filename" | tee -a "$REPORT"
    echo "----------------------------------------" | tee -a "$REPORT"

    total_lines=$(wc -l < "$file")
    data_rows=$((total_lines - 1))

    echo "Data Rows      : $data_rows" | tee -a "$REPORT"

    column_count=$(head -n 1 "$file" | awk -F',' '{print NF}')
    echo "Column Count   : $column_count" | tee -a "$REPORT"

    file_size=$(du -h "$file" | cut -f1)
    echo "File Size      : $file_size" | tee -a "$REPORT"

    header=$(head -n 1 "$file")
    echo "Header         : $header" | tee -a "$REPORT"

    empty_fields=$(grep -o ',,' "$file" | wc -l || true)
    echo "Empty Fields   : $empty_fields" | tee -a "$REPORT"

    echo "First 3 Records:" | tee -a "$REPORT"
    head -n 4 "$file" | tail -n 3 | tee -a "$REPORT"

done

echo "" | tee -a "$REPORT"
echo "========================================" | tee -a "$REPORT"
echo "Profiling Completed Successfully" | tee -a "$REPORT"
echo "Report Saved At:" | tee -a "$REPORT"
echo "$REPORT" | tee -a "$REPORT"
echo "========================================" | tee -a "$REPORT"
