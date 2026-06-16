import pandas as pd
import re
import math
import os

TABLE_NAME = "PreProcessedDataset"

def sanitize_column(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def sql_escape(value):
    if value is None:
        return "NULL"
    if isinstance(value, float) and math.isnan(value):
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"

def convert_csv_to_sql(csv_file: str):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Input CSV not found: {csv_file}")

    output_sql = csv_file.replace(".csv", ".sql")

    print(f"Loading dataset: {csv_file}")

    df = pd.read_csv(csv_file)
    df.columns = [sanitize_column(c) for c in df.columns]

    create_stmt = f"CREATE TABLE {TABLE_NAME} (\n"
    create_stmt += ",\n".join([f"    {c} TEXT" for c in df.columns])
    create_stmt += "\n);\n\n"

    batch_size = 500
    rows = []

    with open(output_sql, "w", encoding="utf-8") as f:
        f.write(create_stmt)

        for i, row in df.iterrows():
            values = ", ".join(sql_escape(v) for v in row.values)
            rows.append(f"({values})")

            if len(rows) >= batch_size:
                f.write(f"INSERT INTO {TABLE_NAME} ({', '.join(df.columns)}) VALUES\n")
                f.write(",\n".join(rows) + ";\n\n")
                rows = []

        if rows:
            f.write(f"INSERT INTO {TABLE_NAME} ({', '.join(df.columns)}) VALUES\n")
            f.write(",\n".join(rows) + ";\n")

    print(f"SQL generated successfully: {output_sql}")


def main():
    # CONFIGURATION LAYER (single source of truth)
    csv_file = "PreProcessedDataset.csv"

    convert_csv_to_sql(csv_file)

    input("Process completed. Press Enter to exit...")


if __name__ == "__main__":
    main()