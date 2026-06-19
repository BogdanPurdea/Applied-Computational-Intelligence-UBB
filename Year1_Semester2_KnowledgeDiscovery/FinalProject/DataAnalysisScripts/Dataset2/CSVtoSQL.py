import pandas as pd
import re
import math
import os

TABLE_NAME = "PreProcessedDataset"

def sanitize_column(name: str) -> str:
    """
    Removes special characters from a column name and replaces them with underscores.
    """
    name = name.strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def sql_escape(value):
    """
    Converts a Python value into a safe string format for SQL insert statements.
    """
    if value is None:
        return "NULL"
    if isinstance(value, float) and math.isnan(value):
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"

def main():
    """
    Loads a CSV dataset, cleans column names, and exports all records into an SQL script.
    """
    csv_file = "Final_Processed_Steel_Data_Clean.csv"

    df = pd.read_csv(csv_file)

    # Clean column names to make them safe for SQL databases
    df.columns = [sanitize_column(c) for c in df.columns]

    # Define the output file path for the full dataset
    output_sql = csv_file.replace(".csv", "_Full.sql")

    with open(output_sql, "w", encoding="utf-8") as f:

        # Write the table creation script
        f.write(f"CREATE TABLE {TABLE_NAME} (\n")
        f.write(",\n".join([f"    {c} VARCHAR(255)" for c in df.columns]))
        f.write("\n);\n\n")

        # Write each row as an individual SQL insert statement
        for _, row in df.iterrows():
            values = ", ".join(sql_escape(v) for v in row.values)
            f.write(f"INSERT INTO {TABLE_NAME} VALUES ({values});\n")

    print(f"Generated SQL file with all records: {output_sql}")
    input("Done. Press Enter to exit...")

if __name__ == "__main__":
    main()
