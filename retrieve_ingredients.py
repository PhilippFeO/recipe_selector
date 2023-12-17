import sys
import os
from ingredient import Ingredient, read_ingredients


def main():
    # Get the number of command-line arguments
    num_args = len(sys.argv)

    # Check if at least one file is provided
    if num_args <= 1:
        print(
            f"Usage: python {os.path.basename(__file__)} recipe_1.yaml ...")
        sys.exit(1)

    # Initialize a superlist to store ingredients from all files
    all_ingredients = []

    # Iterate through command-line arguments starting from the second argument
    for arg_index in range(1, num_args):
        file_path = sys.argv[arg_index]

        # Read ingredients from the current file
        ingredients = read_ingredients(file_path)

        # Append the ingredients to the superlist
        all_ingredients.extend(ingredients)
        all_ingredients = sorted(all_ingredients,
                                 key=lambda ingredient: ingredient.category_weight,
                                 reverse=True)

    # List is saved via ">" operation in main bash script.
    # Print list of ingredients if run directly from command line.
    header = Ingredient.to_table_string()
    print(header)
    print()
    for ingredient in all_ingredients:
        print(ingredient)


if __name__ == "__main__":
    main()
