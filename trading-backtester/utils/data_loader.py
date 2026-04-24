import csv

def load_data(filepath):
    prices = []

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['Close'] != 'null':  # safety check
                prices.append(float(row['Close']))

    return prices