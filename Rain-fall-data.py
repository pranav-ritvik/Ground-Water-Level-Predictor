import pandas as pd

# Load the Excel file
file_path = '/Users/ritvikdunga/Documents/SIH-GWL/Rainfall/2016/SUM.xls'
df = pd.read_excel(file_path, header=[1, 2])  # Read the first two rows as header

# Create new column names by combining the date with 'Actual', 'Normal', and 'Deviation'
df.columns = [f'{col[0]}_{col[1]}' if 'Unnamed' not in col[1] else col[0] for col in df.columns]

# Display the first few rows to confirm the correct column names
print(df.head())

#%%

# Set the 'State' column as the index
df.set_index('STATE', inplace=True)

# Function to safely split column names
def split_column_name(col):
    if isinstance(col, str):  # Only process if col is a string
        parts = col.split('_')
        if len(parts) == 2:
            date_str, metric = parts[0], parts[1].split(' ')[0]  # Handle "01 Jan 2016_Actual (mm)"
            # Convert date_str to datetime
            date = pd.to_datetime(date_str, format='%d %b %Y')
        else:
            date, metric = col, ''  # If no underscore is found, return the original column name
        return date, metric
    else:
        return col  # Return the original column (likely a tuple)

# Apply the function to create a MultiIndex only if needed
if isinstance(df.columns[0], str):  # Check if columns are still strings
    df.columns = pd.MultiIndex.from_tuples(
        [split_column_name(col) for col in df.columns],
        names=['Date', 'Metric']
    )

# Convert relevant columns to numeric, forcing errors to NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Transpose the DataFrame, resample, then transpose back
monthly_avg = df.T.resample('M', level='Date').mean().T

# Display the result
print(monthly_avg)

#%%

# Create a new DataFrame from monthly_avg
df_monthly_avg = monthly_avg.copy()

# Rename the columns to the 'YYYY-MM' format
df_monthly_avg.columns = [col.strftime('%Y-%m') for col in df_monthly_avg.columns]

# Display the result
print(df_monthly_avg)

df_monthly_avg_new = df_monthly_avg.T

#%%

import os
import pandas as pd
from datetime import datetime

# Base directory containing all Rainfall folders
base_dir = '/Users/ritvikdunga/Documents/SIH-GWL/Rainfall/'

# Initialize an empty list to store DataFrames
dfs = []

# Iterate through each folder in the base directory
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        # Construct the full file path to SUM.xls
        file_path = os.path.join(folder_path, 'SUM.xls')
        if os.path.exists(file_path):
            # Load the Excel file
            df = pd.read_excel(file_path, header=[1, 2])  # Read the first two rows as header

            # Create new column names by combining the date with 'Actual', 'Normal', and 'Deviation'
            df.columns = [f'{col[0]}_{col[1]}' if 'Unnamed' not in col[1] else col[0] for col in df.columns]

            # Set the 'State' column as the index
            df.set_index('STATE', inplace=True)

            # Function to safely split column names
            def split_column_name(col):
                if isinstance(col, str):  # Only process if col is a string
                    parts = col.split('_')
                    if len(parts) == 2:
                        date_str, metric = parts[0], parts[1].split(' ')[0]  # Handle "01 Jan 2016_Actual (mm)"
                        # Convert date_str to datetime
                        date = pd.to_datetime(date_str, format='%d %b %Y')
                    else:
                        date, metric = col, ''  # If no underscore is found, return the original column name
                    return date, metric
                else:
                    return col  # Return the original column (likely a tuple)

            # Apply the function to create a MultiIndex only if needed
            if isinstance(df.columns[0], str):  # Check if columns are still strings
                df.columns = pd.MultiIndex.from_tuples(
                    [split_column_name(col) for col in df.columns],
                    names=['Date', 'Metric']
                )

            # Convert relevant columns to numeric, forcing errors to NaN
            df = df.apply(pd.to_numeric, errors='coerce')

            # Transpose the DataFrame, resample, then transpose back
            monthly_avg = df.T.resample('M', level='Date').mean().T

            # Rename the columns to the 'YYYY-MM' format
            monthly_avg.columns = [col.strftime('%Y-%m') for col in monthly_avg.columns]

            # Append to list of DataFrames
            dfs.append(monthly_avg)

# Concatenate all DataFrames along the columns
final_df = pd.concat(dfs, axis=1)

# Drop duplicate columns that may have resulted from concatenation
final_df = final_df.loc[:,~final_df.columns.duplicated()]

# Ensure columns are in date order from '2016-01' to '2022-07'
date_range = pd.date_range(start='2016-01', end='2022-08', freq='M').strftime('%Y-%m')
final_df = final_df.reindex(columns=date_range, fill_value=pd.NA)

# Transpose to have dates as rows and states as columns
final_df_transposed = final_df.T

# Display the final DataFrame
print(final_df_transposed)

#%%

import glob

# Define the base directory path where the subfolders are located
base_directory_path = '/Users/ritvikdunga/Documents/SIH-GWL/Ground Water/'

# Initialize a DataFrame to hold all the combined data with full month range
full_month_range = pd.date_range(start='2016-01', end='2022-08', freq='M').to_period('M')
merged_df = pd.DataFrame({'year_month': full_month_range})

# Loop through each subfolder in the base directory
for folder in glob.glob(base_directory_path + "*/"):
    # Extract folder name for use in column renaming
    folder_name = os.path.basename(os.path.normpath(folder))
    
    print(folder_name)

#%%

import os
import glob
import pandas as pd

# Define the base directory path where the subfolders are located
base_directory_path = '/Users/ritvikdunga/Documents/SIH-GWL/Ground Water/'

# Get the list of folder names from the directory
folder_names = []
for folder in glob.glob(base_directory_path + "*/"):
    # Extract the folder name and normalize it to uppercase
    folder_name = os.path.basename(os.path.normpath(folder)).upper()
    folder_names.append(folder_name)

# Print out the folder names for verification
print("Folder names extracted:", folder_names)

# Filter columns in final_df_transposed to only those matching folder names
filtered_columns = [col for col in final_df_transposed.columns if col.upper() in folder_names]

# Create a new DataFrame with the filtered columns
filtered_df = final_df_transposed[filtered_columns]

# Print the columns in the new DataFrame to verify
print("Filtered DataFrame columns:", filtered_df.columns)

filtered_df_reset = filtered_df.reset_index()

print(f"DataFrame saved to {file_path}")

# Rename column
filtered_df_reset = filtered_df_reset.rename(columns={'index': 'year_month'})

# Convert both 'year_month' columns to string
filtered_df_reset['year_month'] = filtered_df_reset['year_month'].astype(str)
merged_df['year_month'] = merged_df['year_month'].astype(str)

# Merge DataFrames based on the common column
final_df = pd.merge(filtered_df_reset, merged_df , on='year_month', how='outer')

import pandas as pd

# Define the path where you want to save the Excel file
output_file_path = '/Users/ritvikdunga/Documents/SIH-GWL/final_data.xlsx'

# Save the DataFrame to an Excel file
final_df.to_excel(output_file_path, index=False)

# Print confirmation message
print(f'DataFrame successfully saved to {output_file_path}')




