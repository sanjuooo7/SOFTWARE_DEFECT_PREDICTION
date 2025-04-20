import csv

# Specify the path to your CSV file
csv_file_path = 'jm1.csv'

# Open the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        print(row)
        print(len(row))
        break
