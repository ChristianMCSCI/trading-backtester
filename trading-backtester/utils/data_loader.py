import csv

def load_data(filepath):
    prices = []

    # Open CSV file
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)

        # Loop through each row
        for row in reader:
            # Extract "Close" column and convert to float
            prices.append(float(row['Close']))

    return prices