import csv


def read_csv(file_path: str) -> dict[str, tuple[str, str]]:
    """
    Reads a CSV file and returns a dictionary.

    :return: dict containing first entry as `key`, second as `value`.
    """
    csv_dict = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            ingredient, category, url = row
            csv_dict[ingredient] = (category, url)

    return csv_dict


if __name__ == "__main__":
    file_path = 'res/ingredient_category_url.csv'
    result = read_csv(file_path)
    print(result)
