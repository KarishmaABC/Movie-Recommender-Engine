# import pandas as pd

# def clean_data(file_path):
#     data = pd.read_csv(file_path)
#     data = data.dropna()  # Remove nulls
#     return data

import pandas as pd

# Load the uploaded dataset
file_path = "dataset/bollywood_data_set.csv"
data = pd.read_csv(file_path)

# Display initial columns
print("Initial Columns in Dataset:", data.columns)

# Rename columns to match expected names
# Customize as per the actual column names in the dataset
data.rename(columns={
    "movie_name": "title", 
    "plot_description": "genre", 
    "director": "director", 
    "IMDB_rating": "rating"
}, inplace=True)

# Drop unnecessary columns if any (optional)
required_columns = ["title", "genre", "director", "rating"]
data = data[required_columns] if set(required_columns).issubset(data.columns) else data

# Fill missing values (optional)
data.fillna("Unknown", inplace=True)

# Save the processed dataset to a new file
output_path = "dataset/processed_bollywood_data_set.csv"
data.to_csv(output_path, index=False)

print("Processed Dataset Saved:", output_path)
print("Sample Data:\n", data.head())
