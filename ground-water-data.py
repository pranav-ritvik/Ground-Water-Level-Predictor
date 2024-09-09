#%%
import pandas as pd

# Replace with your actual file path
file_path = '/Users/ritvikdunga/Documents/SIH-GWL/Ground Water/Andhra/2016-2018.xlsx'

# Read the Excel file, specifying the correct header row to use (row 5, index 4)
df = pd.read_excel(file_path, header=5)  # Use row index 5 as the header

# Display the first few rows of the DataFrame to confirm correct loading
print(df)

#%%

# Convert the 'date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract the year and month to create a new 'year_month' column
df['year_month'] = df['Date'].dt.to_period('M')

# Group by 'year_month' and calculate the average ground water level
monthly_avg_ground_water_level = df.groupby('year_month')['GW Level(mbgl)'].mean().reset_index()

print(monthly_avg_ground_water_level)


#%%

# Group by 'year_month' and calculate the average ground water level
monthly_avg_ground_water_level = df.groupby('year_month')['GW Level(mbgl)'].mean().reset_index()

# Create a complete range of months for 2016 and 2017
full_month_range = pd.date_range(start='2016-01', end='2018-01', freq='M').to_period('M')

# Convert this range to a DataFrame
full_month_df = pd.DataFrame(full_month_range, columns=['year_month'])

# Merge the existing data with this complete range
merged_df = pd.merge(full_month_df, monthly_avg_ground_water_level, on='year_month', how='left')

# Forward fill missing values to propagate the last observed value forward
merged_df['GW Level(mbgl)'] = merged_df['GW Level(mbgl)'].ffill()

# Rename the column 'GW Level(mbgl)' to 'Average GW Level'
merged_df.rename(columns={'GW Level(mbgl)': 'GW Level AndhraPradesh(mbgl)'}, inplace=True)

print(merged_df)

#%%

import pandas as pd
import glob

# Define the directory path where the Excel files are located
directory_path = '/Users/ritvikdunga/Documents/SIH-GWL/Ground Water/Andhra/'

# Use glob to get all Excel files in the directory
file_paths = glob.glob(directory_path + "*.xlsx")

# Initialize an empty list to store individual DataFrames
df_list = []

# Loop through each file and process it
for file_path in file_paths:
    # Read the Excel file
    df = pd.read_excel(file_path, header=5)

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract the year and month to create a new 'year_month' column
    df['year_month'] = df['Date'].dt.to_period('M')

    # Group by 'year_month' and calculate the average ground water level
    monthly_avg = df.groupby('year_month')['GW Level(mbgl)'].mean().reset_index()

    # Append the processed DataFrame to the list
    df_list.append(monthly_avg)

# Combine all DataFrames in the list into a single DataFrame
combined_df = pd.concat(df_list)

# Create a complete range of months for 2016 to 2022
full_month_range = pd.date_range(start='2016-01', end='2022-08', freq='M').to_period('M')

# Convert this range to a DataFrame
full_month_df = pd.DataFrame(full_month_range, columns=['year_month'])

# Merge the combined data with this complete range
merged_df = pd.merge(full_month_df, combined_df, on='year_month', how='left')

# Forward fill missing values to propagate the last observed value forward
merged_df['GW Level(mbgl)'] = merged_df['GW Level(mbgl)'].ffill()

# Rename the column 'GW Level(mbgl)' to 'GW Level AndhraPradesh(mbgl)'
merged_df.rename(columns={'GW Level(mbgl)': 'GW Level AndhraPradesh(mbgl)'}, inplace=True)

print(merged_df)

#%%

import pandas as pd
import glob
import os

# Define the base directory path where the subfolders are located
base_directory_path = '/Users/ritvikdunga/Documents/SIH-GWL/Ground Water/'

# Initialize a DataFrame to hold all the combined data with full month range
full_month_range = pd.date_range(start='2016-01', end='2022-08', freq='M').to_period('M')
merged_df = pd.DataFrame({'year_month': full_month_range})

# Loop through each subfolder in the base directory
for folder in glob.glob(base_directory_path + "*/"):
    # Extract folder name for use in column renaming
    folder_name = os.path.basename(os.path.normpath(folder))
    
    # Get all Excel files in the current subfolder
    file_paths = glob.glob(folder + "*.xlsx")
    
    # Initialize an empty list to store DataFrames for the current folder
    df_list = []
    
    # Loop through each file in the subfolder and process it
    for file_path in file_paths:
        # Read the Excel file
        df = pd.read_excel(file_path, header=5)

        # Convert the 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Extract the year and month to create a new 'year_month' column
        df['year_month'] = df['Date'].dt.to_period('M')

        # Group by 'year_month' and calculate the average ground water level
        monthly_avg = df.groupby('year_month')['GW Level(mbgl)'].mean().reset_index()

        # Append the processed DataFrame to the list
        df_list.append(monthly_avg)

    # Combine all DataFrames from the current folder into a single DataFrame
    combined_df = pd.concat(df_list)

    # Merge with full month range to ensure all months are represented
    merged_folder_df = pd.merge(merged_df[['year_month']], combined_df, on='year_month', how='left')

    # Forward fill missing values to propagate the last observed value forward
    merged_folder_df['GW Level(mbgl)'] = merged_folder_df['GW Level(mbgl)'].ffill()

    # Add this folder's data to the main DataFrame as a new column
    merged_df[f'GW Level {folder_name}(mbgl)'] = merged_folder_df['GW Level(mbgl)']

# Print the final combined DataFrame
print(merged_df)

#%%
