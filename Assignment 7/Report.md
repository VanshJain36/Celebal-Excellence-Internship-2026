# Incremental Data Processing using Delta Lake in Databricks

## Objective

The objective of this assignment was to implement incremental data processing using Delta Lake in Databricks.

## Dataset

The assignment uses the Sample Superstore dataset. The dataset was divided into two separate files:

* **Initial Dataset:** Contains approximately 50% of the original records and was used for the initial load.
* **Incremental Dataset:** Contains the remaining records along with a few modified records to simulate updates in existing data.

## Implementation Steps

### 1. Initial Data Load

The initial dataset was loaded into Databricks and stored as a Delta table.

### 2. Data Cleaning

Basic data quality checks were performed:

* Removed null values.
* Removed duplicate records.

### 3. Incremental Data Load

A second dataset was created to represent newly arrived data. This dataset contained:

* New records that did not exist in the target table.
* Existing records with modified values to simulate updates.

### 4. Incremental Processing using MERGE

Delta Lake's MERGE operation was used to:

* Update existing records when matching business keys were found.
* Insert new records when no matching key existed.

### 5. Validation

The incremental load was validated using:

* Row count after MERGE.
* Duplicate record checks.
* Delta transaction history.

## Results

* New records were successfully inserted into the Delta table.
* Existing records were successfully updated.
* No duplicate records were introduced during the merge process.
* Delta transaction history confirmed successful execution of the MERGE operation.

## Conclusion

This assignment demonstrates how Delta Lake can be used to implement incremental data processing in Databricks. The implementation follows an SCD Type 1 update pattern where existing records are overwritten with the latest values while new records are inserted into the target table.
