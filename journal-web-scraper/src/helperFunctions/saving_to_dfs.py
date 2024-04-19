import os
import pandas as pd

def process_file(file_path, new_df, columns):
    if os.path.exists(file_path):
        # Read existing data
        existing_df = pd.read_csv(file_path)

        # Append new data
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Drop duplicates
        combined_df.drop_duplicates(subset=columns, inplace=True)
    else:
        # If file doesn't exist, use new data
        combined_df = new_df

    # Save to file
    combined_df.to_csv(file_path, index=False)