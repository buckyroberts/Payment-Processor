import csv
import json


def read_csv(*, file):
    """
    Read CSV file as list of dictionaries
    """

    results = []
    with open(file) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            results.append(row)
    return results


def write_json(*, file, data):
    """
    Write JSON file
    """

    with open(file, 'w') as f:
        json.dump(data, f, indent=2)
