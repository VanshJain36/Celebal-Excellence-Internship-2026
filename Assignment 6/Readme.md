# Spark Data Processing and Performance Optimization

## Objective

This assignment focuses on understanding Apache Spark architecture and implementing efficient data processing techniques using PySpark. The work covers Spark execution concepts, DataFrame transformations, schema management, file format optimization, and performance best practices.

---

## Topics Covered

### Spark Architecture

* Driver Program
* Cluster Manager
* Executors
* Tasks and Stages
* Client Mode vs Cluster Mode

### Spark Execution Concepts

* Lazy Evaluation
* Directed Acyclic Graph (DAG)
* Lineage Graph
* Fault Tolerance

### Data Processing Operations

* Reading CSV and Parquet files
* Explicit Schema Handling
* Filtering and Column Selection
* Data Type Casting
* Renaming Columns
* Creating New Columns
* Handling Null Values

### Performance Concepts

* Narrow vs Wide Transformations
* Shuffle Operations
* Predicate Pushdown
* CSV vs Parquet Performance Comparison
* Best Practices for Large Datasets

---

## Technologies Used

* Apache Spark
* PySpark
* Python 3.10

---

## Assignment Workflow

```text
Read Data
    ↓
Apply Schema
    ↓
Filter Records
    ↓
Transform Data
    ↓
Handle Null Values
    ↓
Write Processed Data
```

---

## Implemented Operations

### File Operations

* Read data from CSV files
* Read data from Parquet files
* Write processed data to CSV
* Write processed data to Parquet

### DataFrame Transformations

* Filter records using conditions
* Select required columns
* Rename columns
* Cast data types
* Add calculated columns
* Handle missing values

---

## Project Structure

```text
spark-assignment/
│
├── data/
│   └── input/
│ 
│
├── notebooks/
│   ├── spark_assignment.ipynb
│   └── spark_assignment theory.docx
|
|
├── output
│   └── parquet file
│
└── README.md
```

---

## Conclusion

This assignment demonstrates the practical application of Spark DataFrame APIs together with core Spark architecture concepts and performance optimization techniques used in real-world data engineering workflows.
