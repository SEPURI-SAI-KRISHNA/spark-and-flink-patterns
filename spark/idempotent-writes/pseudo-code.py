df = read_input()

df_deduped = (
    df
    .withColumn("pk", generate_primary_key(df))
    .dropDuplicates(["pk"])
)

df_deduped.writeTo("iceberg.table") \
    .option("overwrite-mode", "dynamic") \
    .append()
