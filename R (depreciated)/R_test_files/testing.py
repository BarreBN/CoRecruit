import pandas as pd
import json

# Initialize an empty list to store each JSON object
data = []

# Specify the file path using a raw string
file_path = r'C:\Users\Brandon\Documents\Datasets\Dataset\2023.enriched.jsonl'

# Open the .jsonl file and read each line, specifying the encoding as UTF-8
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Parse each line as JSON and append to the list
        data.append(json.loads(line))

# Convert the list of JSON objects to a DataFrame
# pandas will automatically handle flattening of nested structures
jobtech_dataset = pd.json_normalize(data)

# Exclude columns containing only None values
jobtech_dataset = jobtech_dataset.dropna(axis=1, how='all')

# Optionally, limit the DataFrame to a smaller size for demonstration
jobtech_dataset = jobtech_dataset.head(5)

# Iterate over each row and print it
for index, row in jobtech_dataset.iterrows():
    print(f"Row {index}:")
    for col in jobtech_dataset.columns:
        print(f"    {col}: {row[col]}")
    print("\n---\n")  # Separator between rows