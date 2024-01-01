import csv


def read_csv(file_path: str, to_int: bool) -> dict[str, str]:
    """
    Reads a CSV file and returns a dictionary.

    :return: dict containing first entry as `key`, second as `value`.
    """
    csv_dict = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            # Other values indicate comments, etc.
            if len(row) == 2:
                key, value = row
                csv_dict[key] = int(value) if to_int else value

    return csv_dict


if __name__ == "__main__":
    file_path = 'res/ingredient_url.csv'
    result = read_csv(file_path)
    print(result)
