import pandas as pd
import os


def combine_csv_files(csv_files, output_csv):
    dfs = []

    for csv_file in csv_files:
        # Extract try name from file name
        try_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Create multi-index columns with the try name and the categories
        df.columns = pd.MultiIndex.from_product([[try_name], df.columns])

        dfs.append(df)

    # Concatenate all the DataFrames along the columns
    combined_df = pd.concat(dfs, axis=1)

    # Write the combined DataFrame to a new CSV file
    combined_df.to_csv(output_csv, index=False)


# List of CSV files to combine
csv_files = [
    'accuracy_try1.csv',
    'accuracy_try2.csv',
    'accuracy_try3.csv',
    'accuracy_try4.csv',
    'accuracy_try5.csv'
]

# Output CSV file
output_csv = 'combined_accuracy_results.csv'

combine_csv_files(csv_files, output_csv)
