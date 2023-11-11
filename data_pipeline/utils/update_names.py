from pyspark.sql import DataFrame
from typing import Dict


def rename_columns(data: DataFrame, column_mapping: Dict[str, str]) -> DataFrame:
    for old_name, new_name in column_mapping.items():
        data = data.withColumnRenamed(old_name, new_name)
    return data
