import pandas as pd
import numpy as np


class IndustrialDataProcessor:
    """
    A class to preprocess steel factory production logs for lifecycle and failure analysis.
    """

    def process_steel_data(self, input_csv_path: str, output_csv_path: str) -> pd.DataFrame:
        """
        Loads the source dataset, reconstructs the timeline, calculates a tonnage-based RUL,
        filters columns, and applies specific binning and encoding to the features.

        Parameters:
            input_csv_path (str): The path to the raw input CSV file.
            output_csv_path (str): The path where the processed CSV file will be saved.

        Returns:
            pd.DataFrame: The fully transformed and filtered dataset.
        """
        # Load the raw industrial dataset while forcing the sleeve column to be read as string text
        df = pd.read_csv(input_csv_path, dtype={'sleeve': str})

        # Combine date and time strings into a single proper datetime object
        df['datetime_combined'] = pd.to_datetime(df['date'] + ' ' + df['sample_time_continuous_caster'])

        # Sort data chronologically by sleeve identifier and time sequence
        df = df.sort_values(by=['sleeve', 'datetime_combined']).reset_index(drop=True)

        # Fill missing steel weights with zero to ensure a continuous accumulation math process
        df['steel_weight, tonn'] = df['steel_weight, tonn'].fillna(0.0)

        # Calculate running total of steel tons processed through each sleeve
        df['cumulative_tons'] = df.groupby('sleeve')['steel_weight, tonn'].cumsum()

        # Find the maximum total tonnage achieved by each sleeve at its retirement point
        max_tons_per_sleeve = df.groupby('sleeve')['cumulative_tons'].transform('max')

        # Compute the steady, decreasing RUL metric in tons
        df['calculated_RUL_tons'] = max_tons_per_sleeve - df['cumulative_tons']

        # Compute the RUL percentage to assist with the requested binned boundaries
        df['RUL_percentage'] = np.where(
            max_tons_per_sleeve > 0,
            (df['calculated_RUL_tons'] / max_tons_per_sleeve) * 100.0,
            0.0
        )

        # Extract and retain only the specified important columns
        keep_columns = [
            'datetime_combined', 'steel_type', 'cast_in_row', 'workpiece_slice_geometry',
            'alloy_type', 'steel_weight, tonn', 'steel_temperature_grab1, Celsius deg.',
            'resistance, tonn', 'swing_frequency, amount/minute', 'crystallizer_movement, mm',
            'alloy_speed, meter/minute', 'water_consumption, liter/minute',
            'water_temperature_delta, Celsius deg.', 'temperature_measurement1, Celsius deg.',
            'temperature_measurement2, Celsius deg.', 'sleeve', 'num_crystallizer', 'num_stream',
            'calculated_RUL_tons', 'RUL_percentage'
        ]

        # Ensure only columns existing in the dataframe are passed
        valid_columns = [col for col in keep_columns if col in df.columns]
        df = df[valid_columns].copy()

        # Custom bin edges: 0 to 25 is Critical, 25 to 50 is Low, 50 to 75 is Medium, 75 to 100 is Healthy
        rul_bins = [-float('inf'), 25.0, 50.0, 75.0, float('inf')]
        rul_labels = ['Critical', 'Low', 'Medium', 'Healthy']
        df['FCA_BIN'] = pd.cut(df['RUL_percentage'], bins=rul_bins, labels=rul_labels)

        # Encode the RUL bins to integers (Critical=0, Low=1, Medium=2, Healthy=3)
        rul_encoding_map = {'Critical': 0, 'Low': 1, 'Medium': 2, 'Healthy': 3}
        df['FCA_ENCODED'] = df['FCA_BIN'].map(rul_encoding_map)

        # Establish exclusion rule to prevent metadata fields from undergoing 3-class binning
        exclude_from_three_bins = [
            'datetime_combined', 'steel_type', 'workpiece_slice_geometry',
            'alloy_type', 'sleeve', 'calculated_RUL_tons', 'RUL_percentage',
            'FCA_BIN', 'FCA_ENCODED'
        ]

        # Bin and encode all other numeric columns into 3 classes (Low, Medium, High)
        for col in df.columns:
            if col not in exclude_from_three_bins and pd.api.types.is_numeric_dtype(df[col]):
                # Fill missing sensor entries with the column average to allow clean binning
                df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0.0)

                # Check if the column has variance before executing the split
                if df[col].nunique() > 1:
                    # Cut the feature space into three equal-width intervals
                    df[f'{col}_BIN'] = pd.cut(df[col], bins=3, labels=['Low', 'Medium', 'High'])
                    # Assign a strict mechanical label sequence (Low=0, Medium=1, High=2)
                    df[f'{col}_ENCODED'] = df[f'{col}_BIN'].map({'Low': 0, 'Medium': 1, 'High': 2})
                else:
                    # Fallback assignment if a value is uniform throughout the column
                    df[f'{col}_BIN'] = 'Low'
                    df[f'{col}_ENCODED'] = 0

        # Save the finalized dataset back to a clean CSV file
        df.to_csv(output_csv_path, index=False)

        return df


# Class execution block
if __name__ == "__main__":
    processor = IndustrialDataProcessor()
    processed_df = processor.process_steel_data('Dataset.csv', 'Final_Processed_Steel_Data.csv')