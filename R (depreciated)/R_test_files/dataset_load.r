library(jsonlite)

# Replace with your actual file path
file_path <- "path/to/your/file.jsonl"

# Reading the .jsonl file
data <- stream_in(file(file_path))

# To look at the first few rows of your dataset
head(data)

# For a summary of your dataset, which includes statistics for numeric columns and a count of values for factor columns
summary(data)

