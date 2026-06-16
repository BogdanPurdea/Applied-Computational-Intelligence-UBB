import pandas as pd
import re
import math
import os

TABLE_NAME = "PreProcessedDataset"
MAX_ROWS = 100

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

def main():
    csv_file = "PreProcessedDataset.csv"

    df = pd.read_csv(csv_file)

    # limit dataset
    if len(df) > MAX_ROWS:
        df = df.sample(n=MAX_ROWS, random_state=42).reset_index(drop=True)

    df.columns = [sanitize_column(c) for c in df.columns]

    output_sql = csv_file.replace(".csv", "_Max100.sql")

    with open(output_sql, "w", encoding="utf-8") as f:

        # CREATE TABLE
        f.write(f"CREATE TABLE {TABLE_NAME} (\n")
        f.write(",\n".join([f"    {c} VARCHAR(255)" for c in df.columns]))
        f.write("\n);\n\n")

        # INSERT ROW BY ROW (HSQLDB SAFE)
        for _, row in df.iterrows():
            values = ", ".join(sql_escape(v) for v in row.values)
            f.write(f"INSERT INTO {TABLE_NAME} VALUES ({values});\n")

    print(f"Generated Toscana-compatible SQL: {output_sql}")
    input("Done. Press Enter to exit...")

if __name__ == "__main__":
    main()