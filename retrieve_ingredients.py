import sys


def read_ingredients(file_path):
    ingredients = []
    reading_ingredients = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Start reading ingredients after the line containing "## Zutaten"
            if reading_ingredients:
                # Stop reading at the first empty line
                if not line:
                    break
                ingredients.append(line[2:])
            elif "## Zutaten" in line:
                reading_ingredients = True

    return ingredients


def main():
    # Get the number of command-line arguments
    num_args = len(sys.argv)

    # Check if at least one file is provided
    if num_args <= 1:
        print("Usage: python script.py file1.md file2.md ...")
        sys.exit(1)

    # Initialize a superlist to store ingredients from all files
    superlist = []

    # Iterate through command-line arguments starting from the second argument
    for arg_index in range(1, num_args):
        file_path = sys.argv[arg_index]

        # Read ingredients from the current file
        ingredients = read_ingredients(file_path)

        # Append the ingredients to the superlist
        superlist.append(ingredients)

    # Print the superlist
    print("===== Per file list of Ingredients =====")
    for index, ingredients in enumerate(superlist, start=1):
        print(f"\n{sys.argv[index].split('/')[1]}:")
        for ingredient in ingredients:
            print(f"- {ingredient}")


if __name__ == "__main__":
    main()
