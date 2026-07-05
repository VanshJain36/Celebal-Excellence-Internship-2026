# Databricks notebook source
df = spark.read.csv(
    '/Workspace/Users/vanshkrjain@gmail.com/data/Sample - Superstore.csv',
    header = True,
    inferSchema = True
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Basic cleaning operations

# COMMAND ----------

df = df.dropna().dropDuplicates()

# COMMAND ----------

df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Storing first(initial) dataset

# COMMAND ----------

df.write.format('delta')\
    .mode('overwrite') \
    .option('delta.columnMapping.mode', 'name') \
    .saveAsTable('workspace.default.superstore_delta')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating incrementla dataset

# COMMAND ----------

incremental_df = spark.read.csv(
    "/Workspace/Users/vanshkrjain@gmail.com/data/superstore_incremental.csv",
    header = True,
    inferSchema = True
    )

# COMMAND ----------

incremental_df = incremental_df.dropna().dropDuplicates()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Performing incremental loading

# COMMAND ----------

from delta.tables import DeltaTable

delta_table = DeltaTable.forName(
    spark,
    'workspace.default.superstore_delta'
)

delta_table.alias('source_table').merge(
    incremental_df.alias('incremental_table'),
    "source_table.'Order ID' = incremental_table.'Order ID'"
 ).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Checking for incremental loading

# COMMAND ----------

incremental = delta_table.toDF().count()
print(f'Rows after merge: {incremental}')

# COMMAND ----------

display(delta_table.history())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Duplicate check

# COMMAND ----------

duplicates = delta_table.toDF().dropDuplicates().show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Final dataset

# COMMAND ----------

delta_table.toDF().show()