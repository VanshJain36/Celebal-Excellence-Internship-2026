# Databricks notebook source
df = spark.read.csv(
    "/Workspace/Users/vanshkrjain@gmail.com/data/Sample - Superstore.csv",
    header=True,
    inferSchema=True
)

# COMMAND ----------

df.show()

# COMMAND ----------

from pyspark.sql.functions import col

df.filter(col('Sub-Category') == 'Appliances')\
    .select('Product ID', 'Profit')\
        .show()

# COMMAND ----------

df_revised = (df.withColumnRenamed("Postal Code","Zip Code")
.withColumn('Profit', col('Profit').cast('double'))
)

# COMMAND ----------

df_revised.printSchema()
df_revised.show()

# COMMAND ----------

df_orders = df.filter(
    (col('Ship Mode') == 'Second Class') &
    (col('Profit') > 1000)
).show()

# COMMAND ----------

df_updated = df.withColumn(
    'Final Profit',
    col('Profit') * 1.18
)

# COMMAND ----------

df_updated.write.format('parquet')\
    .mode('overwrite')\
    .save('/Volumes/workspace/default/data_files/superstore_updated')

# COMMAND ----------

spark.read.parquet('/Volumes/workspace/default/data_files/superstore_updated')\
    .filter(col("Customer ID").isNotNull())\
    .write.mode('overwrite')\
    .option('header', True)\
    .csv('/Volumes/workspace/default/data_files/superstore_updated_csv')

# COMMAND ----------

df.filter(
    (col('Region') == 'North') |
    (col('Ship Mode') == 'First Class')
).show()