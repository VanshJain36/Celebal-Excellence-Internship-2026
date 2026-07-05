# Incremental Data Processing using Delta Lake

## Assignment Overview

This assignment demonstrates incremental data processing using Delta Lake in Databricks with the Sample Superstore dataset.

The objective of the assignment is to simulate a real-world incremental ingestion pipeline where new records are inserted and existing records are updated using Delta Lake's MERGE functionality.

## Tech Stack

* Databricks Community Edition
* PySpark
* Delta Lake
* SQL

## Dataset

Dataset used:

* Sample Superstore Dataset

The dataset was split into two parts:

### Initial Load Dataset

Contains approximately 50% of the original records and is used to create the initial Delta table.

### Incremental Dataset

Contains:

* Remaining records from the original dataset.
* Modified records to simulate updates to existing data.

## Assignment Workflow

```text
Sample Superstore Dataset
            │
            ├── Initial Load Dataset (50%)
            │         ↓
            │   Data Cleaning
            │         ↓
            │   Delta Table Creation
            │
            └── Incremental Dataset
                      ↓
                 Data Cleaning
                      ↓
                  MERGE INTO
                      ↓
               Updated Delta Table
                      ↓
                  Validation
```

## Features Implemented

* Initial data ingestion
* Data cleaning
* Duplicate removal
* Incremental data simulation
* Delta Lake MERGE operation
* Insert and update handling
* Validation checks
* Transaction history verification

## Validation Performed

* Row count verification
* Duplicate checks
* Updated record validation
* New record validation
* Delta transaction history check

## SCD Implementation

The assignment follows an SCD Type 1 approach where:

* Existing records are overwritten with new values.
* Historical versions of records are not maintained.

## Repository Structure

```text
├── notebooks/
│   ├── delta_scd_assignment_notebook
│   └── source_code.py
│
├── datasets/
│   ├── sample_superstore.csv
│   └── incremental_superstore.csv
│
├── screenshots/
│   ├── data_cleaning.png
│   ├── data_loading.png
│   ├── SCD1.png
│   ├── validation.png
│   └── final_output.png
│
└── README.md
```

## Conclusion

This assignment demonstrates a practical implementation of incremental data processing using Delta Lake in Databricks.
