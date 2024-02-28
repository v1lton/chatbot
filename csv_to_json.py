import csv
import json

csv_file_path = 'questions_and_answers.csv'
json_file_path = 'questions_and_answers.json'

# Read the CSV and add the data to a dictionary
data = []
with open(csv_file_path, encoding='utf-8') as csvf:
    csv_reader = csv.DictReader(csvf)
    for rows in csv_reader:
        data.append(rows)

# Write the data to a JSON file
with open(json_file_path, 'w', encoding='utf-8') as jsonf:
    jsonf.write(json.dumps(data, indent=4))
