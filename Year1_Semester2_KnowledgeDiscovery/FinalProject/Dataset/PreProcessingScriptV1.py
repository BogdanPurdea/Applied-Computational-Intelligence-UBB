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

    def parse_temporal_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts date and time columns into combined timestamp objects.
        Extracts year, month, day, hour, and shift variables into new columns.
        Retains the original text-based time columns.
        Returns the DataFrame with appended temporal features.
        """
        # Convert the primary date column, coercing errors to NaT
        df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")

        time_columns = [
            "time_temperature_measurement1",
            "time_temperature_measurement2",
            "sample_time_continuous_caster"
        ]

        # Standardize empty time values
        for col in time_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().replace("nan", np.nan)

        # Create a unified timestamp column
        df["timestamp"] = pd.to_datetime(
            df["date"].astype(str) + " " + df["sample_time_continuous_caster"].astype(str),
            errors="coerce"
        )

        # Extract numeric date components
        df["year"] = df["timestamp"].dt.year
        df["month"] = df["timestamp"].dt.month
        df["day"] = df["timestamp"].dt.day
        df["hour"] = df["timestamp"].dt.hour
        df["weekday"] = df["timestamp"].dt.weekday

        # Group hours into distinct work shifts
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
            # Convert to string to ensure the encoder can process mixed types or 0s
            df[encoded_col] = encoder.fit_transform(df[col].astype(str))
            self.label_encoders[col] = encoder

        return df

    def scale_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies StandardScaler to numerical columns.
        Appends the scaled results as new columns with the '_scaled' suffix.
        Excludes specific target and identifier columns from scaling.
        Returns the updated DataFrame.
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        exclude_cols = [
            "RUL",
            "sleeve",
            "num_crystallizer",
            "num_stream"
        ]

        # Filter out excluded columns and already scaled/encoded columns
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
                # Divide data into 3 equal-sized quantiles
                df[fca_col] = pd.qcut(
                    df[col],
                    q=3,
                    labels=["Low", "Medium", "High"],
                    duplicates="drop"
                )
            except Exception:
                # Fallback if the column lacks variance (e.g., filled entirely with 0s)
                df[fca_col] = "Constant"

        # Discretize the specific RUL target variable
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
        df = self.parse_temporal_data(df)
        df = self.convert_numeric_columns(df)

        df = self.fill_missing_data(df)

        df = self.add_industrial_features(df)
        df = self.encode_categorical_columns(df)
        df = self.scale_numeric_features(df)
        df = self.discretize_for_fca(df)

        df = self.fill_missing_data(df)

        self.save_data(df)

        print(f"Final shape: {df.shape}")
        print(f"Saved preprocessed dataset to: {self.output_path}")

# Script execution sequence
if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent

    processor = DatasetPreprocessor(
        input_path=script_dir / "Dataset.csv",
        output_path=script_dir / "PreProcessedDataset.csv"
    )
    processor.process()