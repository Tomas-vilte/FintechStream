from pyspark.sql import DataFrame


def rename_columns(df: DataFrame, column_mapping: dict) -> DataFrame:
    for topic, columns in column_mapping.items():
        for current_name, new_name in columns.items():
            df = df.withColumnRenamed(current_name, new_name)
    return df
