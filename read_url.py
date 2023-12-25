import csv


def read_ingredient_url_csv(file_path) -> dict[str, str]:
    """
    Reads ingredient and it url from a `csv` file.

    :return: dict containing ingredient as `key`, `url` as value
    """
    urls = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if len(row) == 2:
                key, value = row
                urls[key] = value

    return urls


if __name__ == "__main__":
    file_path = 'ingredient_url.csv'
    result = read_ingredient_url_csv(file_path)
    print(result)
