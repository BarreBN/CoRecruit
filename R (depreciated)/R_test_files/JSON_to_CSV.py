import json
import pandas as pd

# Load JSON data
with open('C:/Users/Brandon/Documents/sustAIn/sustAIn/R/subset_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define the fields we want to extract
fields = [
    'description.text', 'workplace_address.city', 'driving_license_required',
    'employment_type.label', 'working_hours_type.label'
]

# Initialize a list to store the processed data
processed_data = []

# Iterate through each job entry
for entry in data:
    processed_entry = {}
    for field in fields:
        keys = field.split('.')
        value = entry
        for key in keys:
            value = value.get(key, None)
            if value is None:
                break
        processed_entry[field.replace('.', '_')] = value
    processed_data.append(processed_entry)

# Create a DataFrame
df = pd.DataFrame(processed_data)

# Replace None with 'No' for the 'driving_license_required' to align with your assumptions
df['driving_license_required'] = df['driving_license_required'].fillna('No')

# Save to CSV
df.to_csv('job_data.csv', index=False)

print("CSV file has been created successfully.")