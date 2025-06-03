#!/usr/bin/env python
# coding: utf-8

# # Data Clean

# In[ ]:


import pandas as pd

# Load the CSV file
file_path = r"D:\Power BI project\startup_funding.csv"
df = pd.read_csv(file_path)

# Basic Cleaning Steps
df.columns = df.columns.str.strip().str.lower()  # Clean column names
df = df.drop_duplicates()  # Remove duplicate rows
df = df.dropna(how='all')  # Drop rows where all values are NaN
df = df.fillna('')  # Replace remaining NaNs with empty strings

# Trim whitespace from string columns
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].str.strip()

# Save the cleaned data to a new CSV file
cleaned_file_path = r"D:\Power BI project\startup_funding_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned and saved to: {cleaned_file_path}")


# # Odd startup names removed

# In[13]:


import pandas as pd

# Load the CSV
file_path = r"D:\Power BI project\startup_funding_final.csv"
df = pd.read_csv(file_path)

# Ensure column exists and clean text
df['startup name'] = df['startup name'].astype(str).str.strip().str.lower()

# List of odd/invalid values
odd_values = ['n/a', 'na', '-', 'unknown', 'none', 'null', '']

# Remove rows with invalid or missing startup names
df = df[~df['startup name'].isin(odd_values)]
df = df[~df['startup name'].str.fullmatch(r'\d+')]  # Remove purely numeric names

# Optional: Reformat to title case
df['startup name'] = df['startup name'].str.title()

# Save the cleaned file
cleaned_path = r"D:\Power BI project\startup_funding_cleaned_final.csv"
df.to_csv(cleaned_path, index=False)

print(f"Odd startup names removed. Cleaned data saved to: {cleaned_path}")


# # formats in 'Date' column to dd/mm/yyyy

# # Remove rows with missing or invalid 'investors name'

# # Convert 'amount in usd' column from USD to INR

# In[16]:


import pandas as pd

# Load the dataset
file_path = r"D:\Power BI project\startup_funding_cleaned_final.csv"
df = pd.read_csv(file_path)

# --- 1. Normalize inconsistent formats in 'Date' column to dd/mm/yyyy ---
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=False)
df = df.dropna(subset=['Date'])
df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

# --- 2. Remove rows with missing or invalid 'investors name' ---
df['investors name'] = df['investors name'].astype(str).str.strip().str.lower()
invalid_investors = ['n/a', 'na', '-', 'unknown', 'none', 'null', '']
df = df[~df['investors name'].isin(invalid_investors)]
df = df[df['investors name'] != '']

# --- 3. Convert 'amount in usd' column from USD to INR ---
usd_to_inr = 83  # Conversion rate (update if needed)
df['amount in usd'] = df['amount in usd'].astype(str).str.replace('[\$,]', '', regex=True)
df['amount in usd'] = pd.to_numeric(df['amount in usd'], errors='coerce')
df['amount in inr'] = df['amount in usd'] * usd_to_inr

# Save the cleaned file
processed_path = r"D:\Power BI project\startup_funding_final_processed.csv"
df.to_csv(processed_path, index=False)

print(f"Cleaned data saved to: {processed_path}")


# # Insert 'Year' column right after 'Date'

# In[17]:


import pandas as pd

# Load the processed CSV
file_path = r"D:\Power BI project\startup_funding_final_processed.csv"
df = pd.read_csv(file_path)

# Convert 'Date' column back to datetime to extract year
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Extract year as string
df['Year'] = df['Date'].dt.year.astype('Int64')  # Keeps NA as <NA>

# Insert 'Year' column right after 'Date'
date_index = df.columns.get_loc('Date')
df.insert(date_index + 1, 'Year', df.pop('Year'))

# Save the updated dataframe
df.to_csv(file_path, index=False)

print(f"'Year' column added next to 'Date'. File updated at: {file_path}")


# #  Keep only rows where 'startup name' matches the pattern

# In[18]:


import pandas as pd

file_path = r"D:\Power BI project\startup_funding_final_processed.csv"
df = pd.read_csv(file_path)

# Clean 'startup name' column: strip spaces and lowercase for checking
df['startup name'] = df['startup name'].astype(str).str.strip()

# Define a regex pattern that allows only typical name characters:
# Letters (including spaces and dots/apostrophes for names like "O'Neil", "St. John")
pattern = r"^[a-zA-Z\s\.\']+$"

# Keep only rows where 'startup name' matches the pattern
df = df[df['startup name'].str.match(pattern)]

# Remove empty names after matching
df = df[df['startup name'] != '']

# Save the cleaned file
cleaned_path = r"D:\Power BI project\startup_funding_final_processed_cleaned.csv"
df.to_csv(cleaned_path, index=False)

print(f"Rows with invalid 'startup name' removed. Cleaned file saved at: {cleaned_path}")


# In[ ]:




