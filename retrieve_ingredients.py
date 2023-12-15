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
                                 key=lambda ingredient: ingredient.category)

    # Save list of ingredients
    # find longest element for proper formatting of the output
    max_len_name = max((len(i.name) for i in all_ingredients)) + 2
    # Print a header/column names
    header = ' '.join((fn.ljust(max_len_name)
                      for fn in Ingredient.field_names))
    print(header)
    print('-' * len(header))
    # Print rows
    for ingredient in all_ingredients:
        # apply padding according to longest entry in table
        print(ingredient.name.ljust(max_len_name),
              ingredient.amount.ljust(max_len_name),
              ingredient.category.ljust(max_len_name),
              ingredient.optional)

    # TODO: Write table into text file <15-12-2023>
    # TODO: Add name of recipe to each ingredient <15-12-2023>
    #   Maybe by adding a recipe attribute to the Ingredient class
    # TODO: Add weight to each ingredient to sort according to order in supermarket <15-12-2023>
    #   fi. vegetables and fruits come first, then diary, etc.
    # TODO: Add method similar to __str__ to Ingredient to construct the string for printing. This method might take one argument, the padding length, in my case max_len_name <15-12-2023>
        # TODO: return this string in __str__ <15-12-2023>


if __name__ == "__main__":
    main()
