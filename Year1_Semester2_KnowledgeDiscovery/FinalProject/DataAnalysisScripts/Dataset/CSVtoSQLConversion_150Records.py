import pandas as pd
import re
import math
import os

TABLE_NAME = "PreProcessedDataset"
TARGET_ROWS = 170000
REQUIRED_SHIFTS = {"Morning", "Afternoon", "Night"}

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

    # -----------------------------
    # Normalize timestamp + shift
    # -----------------------------
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Remove invalid timestamps
    df = df.dropna(subset=["timestamp"])

    # Extract date for grouping
    df["date"] = df["timestamp"].dt.date

    selected_rows = []

    # Group by day
    for day, group in df.groupby("date"):

        shifts_present = set(group["shift"].dropna().unique())

        # strict completeness rule
        if not REQUIRED_SHIFTS.issubset(shifts_present):
            continue

        # enforce deterministic ordering
        day_rows = []

        for shift in ["Morning", "Afternoon", "Night"]:
            match = group[group["shift"] == shift]

            if match.empty:
                break

            # take first record of that shift
            day_rows.append(match.iloc[0])

        if len(day_rows) == 3:
            selected_rows.extend(day_rows)

        if len(selected_rows) >= TARGET_ROWS:
            selected_rows = selected_rows[:TARGET_ROWS]
            break

    # Build final dataframe
    df_final = pd.DataFrame(selected_rows)

    # Drop helper column
    df_final = df_final.drop(columns=["date"])

    # -----------------------------
    # SQL EXPORT (Toscana-safe)
    # -----------------------------
    df_final.columns = [sanitize_column(c) for c in df_final.columns]

    output_sql = csv_file.replace(".csv", "_Max_Shift_Balanced.sql")

    with open(output_sql, "w", encoding="utf-8") as f:

        f.write(f"CREATE TABLE {TABLE_NAME} (\n")
        f.write(",\n".join([f"    {c} VARCHAR(255)" for c in df_final.columns]))
        f.write("\n);\n\n")

        for _, row in df_final.iterrows():
            values = ", ".join(sql_escape(v) for v in row.values)
            f.write(f"INSERT INTO {TABLE_NAME} VALUES ({values});\n")

    print(f"Generated balanced SQL dataset: {output_sql}")
    print(f"Final row count: {len(df_final)}")
    input("Done. Press Enter to exit...")

if __name__ == "__main__":
    main()