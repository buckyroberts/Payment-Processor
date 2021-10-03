import csv


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
