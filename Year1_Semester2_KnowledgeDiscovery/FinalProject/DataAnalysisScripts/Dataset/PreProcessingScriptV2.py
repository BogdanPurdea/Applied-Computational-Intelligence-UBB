from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DatasetPreprocessor:
    """
    Executes a comprehensive data preprocessing pipeline on a CSV dataset.
    Retains all original rows and columns. Appends transformed features as new columns.
    """

    def __init__(self, input_path: str, output_path: str):
        """
        Initializes the preprocessor with specified input and output file paths.
        Instantiates required encoders and scalers.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.label_encoders = {}
        self.scaler = StandardScaler()

    def load_data(self) -> pd.DataFrame:
        """
        Reads the CSV file into a pandas DataFrame.
        Returns the loaded DataFrame.
        """
        return pd.read_csv(self.input_path)

    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes leading whitespace, trailing whitespace, and quote characters from column headers.
        Returns the DataFrame with cleaned column headers.
        """
        df.columns = (
            df.columns
            .str.strip()
            .str.replace('"', '', regex=False)
            .str.replace("'", "", regex=False)
        )
        return df

    def normalize_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts completely empty strings or strings containing only whitespace into standard NaN values.
        Returns the normalized DataFrame.
        """
        return df.replace(r"^\s*$", np.nan, regex=True)

    def deduplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes exact duplicate rows, keeping only the first occurrence.
        Deduplication is performed on the original raw columns (before any
        derived / encoded / scaled columns are added) so that only genuinely
        identical source records are dropped.
        Returns the deduplicated DataFrame and prints a removal summary.
        """
        before = len(df)
        df = df.drop_duplicates(keep="first").reset_index(drop=True)
        removed = before - len(df)
        print(f"[Deduplication] Removed {removed} duplicate row(s). Rows remaining: {len(df)}")
        return df

    def parse_temporal_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts date and time columns into combined timestamp objects.
        Extracts year, month, day, hour, and shift variables into new columns.
        Retains the original text-based time columns.
        Returns the DataFrame with appended temporal features.
        """
        df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")

        time_columns = [
            "time_temperature_measurement1",
            "time_temperature_measurement2",
            "sample_time_continuous_caster"
        ]

        for col in time_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().replace("nan", np.nan)

        df["timestamp"] = pd.to_datetime(
            df["date"].astype(str) + " " + df["sample_time_continuous_caster"].astype(str),
            errors="coerce"
        )

        df["year"] = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month
        df["day"] = df["timestamp"].dt.day
        df["hour"] = df["timestamp"].dt.hour
        df["weekday"] = df["timestamp"].dt.weekday

        df["shift"] = pd.cut(
            df["hour"],
            bins=[-1, 7, 15, 23],
            labels=["Night", "Morning", "Afternoon"]
        )

        return df

    def convert_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Forces numeric conversion on all columns not explicitly listed as categorical or temporal.
        Returns the DataFrame with updated data types.
        """
        non_numeric_cols = [
            "date",
            "date_parsed",
            "timestamp",
            "time_temperature_measurement1",
            "time_temperature_measurement2",
            "sample_time_continuous_caster",
            "steel_type",
            "doc_requirement",
            "workpiece_slice_geometry",
            "alloy_type",
            "kind",
            "shift"
        ]

        for col in df.columns:
            if col not in non_numeric_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    def fill_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Replaces all missing, null, or NaT values in the DataFrame with the integer 0.
        Returns the imputed DataFrame.
        """
        return df.fillna(0)

    def encode_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies Label Encoding to text-based categorical columns.
        Appends the encoded numeric results as new columns with the '_encoded' suffix.
        Returns the updated DataFrame.
        """
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns

        for col in categorical_cols:
            encoded_col = f"{col}_encoded"
            encoder = LabelEncoder()
            df[encoded_col] = encoder.fit_transform(df[col].astype(str))
            self.label_encoders[col] = encoder

        return df

    def scale_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies StandardScaler to numerical columns.
        Appends the scaled results as new columns with the '_scaled' suffix.
        Excludes specific identifier columns from scaling. RUL is included for scaling.
        Returns the updated DataFrame.
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Target column RUL is removed from this list so that RUL_scaled is created.
        exclude_cols = [
            "sleeve",
            "num_crystallizer",
            "num_stream"
        ]

        numeric_cols = [
            col for col in numeric_cols
            if col not in exclude_cols
            and not col.endswith("_encoded")
            and not col.endswith("_scaled")
        ]

        if numeric_cols:
            scaled_values = self.scaler.fit_transform(df[numeric_cols])

            for i, col in enumerate(numeric_cols):
                df[f"{col}_scaled"] = scaled_values[:, i]

        return df

    def discretize_for_fca(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups numerical continuous data into distinct bins for Formal Concept Analysis.
        Appends the categorized data as new columns with the '_fca_bin' suffix.
        Returns the updated DataFrame.
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        exclude_cols = [
            "sleeve",
            "num_crystallizer",
            "num_stream"
        ]

        numeric_cols = [
            col for col in numeric_cols
            if col not in exclude_cols
            and not col.endswith("_encoded")
            and not col.endswith("_scaled")
            and not col.endswith("_fca_bin")
        ]

        for col in numeric_cols:
            fca_col = f"{col}_fca_bin"

            try:
                df[fca_col] = pd.qcut(
                    df[col],
                    q=3,
                    labels=["Low", "Medium", "High"],
                    duplicates="drop"
                )
            except Exception:
                df[fca_col] = "Constant"

        if "RUL" in df.columns:
            df["RUL_class"] = pd.cut(
                df["RUL"],
                bins=[-1, 150, 400, 800, np.inf],
                labels=["Critical", "Low", "Medium", "Healthy"]
            )

        return df

    def add_industrial_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates specific domain-knowledge features from the raw data.
        Appends the calculated metrics as new columns.
        Returns the updated DataFrame.
        """
        if {
            "temperature_measurement1, Celsius deg.",
            "temperature_measurement2, Celsius deg."
        }.issubset(df.columns):
            df["temperature_difference"] = (
                df["temperature_measurement1, Celsius deg."]
                - df["temperature_measurement2, Celsius deg."]
            )

        cooling_cols = [
            "water_consumption, liter/minute",
            "water_consumption_secondary_cooling_zone_num1, liter/minute",
            "water_consumption_secondary_cooling_zone_num2, liter/minute",
            "water_consumption_secondary_cooling_zone_num3, liter/minute"
        ]

        existing_cooling_cols = [col for col in cooling_cols if col in df.columns]

        if existing_cooling_cols:
            df["total_cooling_consumption"] = df[existing_cooling_cols].sum(axis=1)
            df["average_cooling_consumption"] = df[existing_cooling_cols].mean(axis=1)

        chemistry_cols = [
            "S, %",
            "P, %",
            "As, %",
            "Pb, %",
            "Sn, %"
        ]

        existing_chemistry_cols = [col for col in chemistry_cols if col in df.columns]

        if existing_chemistry_cols:
            df["impurity_index"] = df[existing_chemistry_cols].sum(axis=1)

        return df

    # Exact output column order required by the downstream pipeline.
    OUTPUT_COLUMNS: list = [
        "RUL", "sleeve", "num_crystallizer", "num_stream", "timestamp", "shift",
        "steel_type_encoded", "doc_requirement_encoded", "workpiece_slice_geometry_encoded",
        "alloy_type_encoded", "kind_encoded", "shift_encoded",
        "workpiece_weight, tonn_scaled", "cast_in_row_scaled",
        "steel_weight_theoretical, tonn_scaled", "slag_weight_close_grab1, tonn_scaled",
        "metal_residue_grab1, tonn_scaled", "steel_weight, tonn_scaled",
        "residuals_grab2, tonn_scaled", "technical_trim, tonn_scaled",
        "grab1_num_scaled", "steel_temperature_grab1, Celsius deg._scaled",
        "grab2_num_scaled", "resistance, tonn_scaled",
        "swing_frequency, amount/minute_scaled", "crystallizer_movement, mm_scaled",
        "alloy_speed, meter/minute_scaled", "water_consumption, liter/minute_scaled",
        "water_temperature_delta, Celsius deg._scaled",
        "water_consumption_secondary_cooling_zone_num1, liter/minute_scaled",
        "water_consumption_secondary_cooling_zone_num2, liter/minute_scaled",
        "water_consumption_secondary_cooling_zone_num3, liter/minute_scaled",
        "quantity, tonn_scaled",
        "temperature_measurement1, Celsius deg._scaled",
        "temperature_measurement2, Celsius deg._scaled",
        "Ce, %_scaled", "C, %_scaled", "Si, %_scaled", "Mn,%_scaled",
        "S, %_scaled", "P, %_scaled", "Cr, %_scaled", "Ni, %_scaled",
        "Cu, %_scaled", "As, %_scaled", "Mo, %_scaled", "Nb, %_scaled",
        "Sn, %_scaled", "Ti, %_scaled", "V, %_scaled", "Al, %_scaled",
        "Ca, %_scaled", "N, %_scaled", "Pb, %_scaled", "Mg, %_scaled",
        "Zn, %_scaled", "RUL_scaled",
        "temperature_difference_scaled", "total_cooling_consumption_scaled",
        "average_cooling_consumption_scaled", "impurity_index_scaled",
        "workpiece_weight, tonn_fca_bin", "cast_in_row_fca_bin",
        "steel_weight_theoretical, tonn_fca_bin", "slag_weight_close_grab1, tonn_fca_bin",
        "metal_residue_grab1, tonn_fca_bin", "steel_weight, tonn_fca_bin",
        "residuals_grab2, tonn_fca_bin", "technical_trim, tonn_fca_bin",
        "grab1_num_fca_bin", "steel_temperature_grab1, Celsius deg._fca_bin",
        "grab2_num_fca_bin", "resistance, tonn_fca_bin",
        "swing_frequency, amount/minute_fca_bin", "crystallizer_movement, mm_fca_bin",
        "alloy_speed, meter/minute_fca_bin", "water_consumption, liter/minute_fca_bin",
        "water_temperature_delta, Celsius deg._fca_bin",
        "water_consumption_secondary_cooling_zone_num1, liter/minute_fca_bin",
        "water_consumption_secondary_cooling_zone_num2, liter/minute_fca_bin",
        "water_consumption_secondary_cooling_zone_num3, liter/minute_fca_bin",
        "quantity, tonn_fca_bin",
        "temperature_measurement1, Celsius deg._fca_bin",
        "temperature_measurement2, Celsius deg._fca_bin",
        "Ce, %_fca_bin", "C, %_fca_bin", "Si, %_fca_bin", "Mn,%_fca_bin",
        "S, %_fca_bin", "P, %_fca_bin", "Cr, %_fca_bin", "Ni, %_fca_bin",
        "Cu, %_fca_bin", "As, %_fca_bin", "Mo, %_fca_bin", "Nb, %_fca_bin",
        "Sn, %_fca_bin", "Ti, %_fca_bin", "V, %_fca_bin", "Al, %_fca_bin",
        "Ca, %_fca_bin", "N, %_fca_bin", "Pb, %_fca_bin", "Mg, %_fca_bin",
        "Zn, %_fca_bin", "RUL_fca_bin",
        "year_fca_bin", "month_fca_bin", "day_fca_bin", "hour_fca_bin",
        "weekday_fca_bin",
        "temperature_difference_fca_bin", "total_cooling_consumption_fca_bin",
        "average_cooling_consumption_fca_bin", "impurity_index_fca_bin",
        "RUL_class",
    ]

    def select_output_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retains and reorders DataFrame columns to exactly match OUTPUT_COLUMNS.
        Columns listed in OUTPUT_COLUMNS that are absent from the DataFrame are
        skipped with a warning so the script never raises a KeyError.
        Returns the filtered, reordered DataFrame.
        """
        available = [col for col in self.OUTPUT_COLUMNS if col in df.columns]
        missing   = [col for col in self.OUTPUT_COLUMNS if col not in df.columns]
        if missing:
            print(f"[Column selection] WARNING – {len(missing)} requested column(s) not found "
                  f"and will be omitted: {missing}")
        print(f"[Column selection] Keeping {len(available)} of {len(self.OUTPUT_COLUMNS)} "
              f"requested columns.")
        return df[available]

    def save_data(self, df: pd.DataFrame) -> None:
        """
        Writes the processed DataFrame to a CSV file at the specified output path.
        Returns None.
        """
        df.to_csv(self.output_path, index=False)

    def process(self) -> None:
        """
        Executes the ordered sequence of preprocessing operations.
        Outputs row count metrics to the console.
        Returns None.
        """
        df = self.load_data()
        print(f"Initial shape: {df.shape}")

        df = self.clean_column_names(df)
        df = self.normalize_missing_values(df)

        # Deduplication is done on raw columns before any derived features are
        # added so that only genuinely identical source records are removed.
        df = self.deduplicate(df)

        df = self.parse_temporal_data(df)
        df = self.convert_numeric_columns(df)

        df = self.fill_missing_data(df)

        df = self.add_industrial_features(df)
        df = self.encode_categorical_columns(df)
        df = self.scale_numeric_features(df)
        df = self.discretize_for_fca(df)

        df = self.fill_missing_data(df)

        # Keep only the required output columns in the specified order.
        df = self.select_output_columns(df)

        self.save_data(df)

        print(f"Final shape: {df.shape}")
        print(f"Saved preprocessed dataset to: {self.output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent

    processor = DatasetPreprocessor(
        input_path=script_dir / "Dataset.csv",
        output_path=script_dir / "PreProcessedDataset.csv"
    )
    processor.process()