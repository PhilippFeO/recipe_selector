import sys
import os
from ingredient import Ingredient, read_ingredients
from read_url import read_ingredient_url_csv
from open_urls import open_ingredient_urls


def retrieve_ingredients():
    """
    This function is called via `python3 retrieve_ingredients recipe-1.yaml ...`. Hence, reading and checking `sys.argv`.
    """
    # Get the number of command-line arguments
    num_args = len(sys.argv)

    # Check if at least one file is provided
    if num_args <= 1:
        print(
            f"Usage: python {os.path.basename(__file__)} recipe_1.yaml ...")
        sys.exit(1)

    # Initialize a superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []

    # Iterate through command-line arguments starting from the second argument
    for arg_index in range(1, num_args):
        file_path = sys.argv[arg_index]
        print(file_path)

        # Read ingredients from the current file
        ingredients = read_ingredients(file_path)

        # Append the ingredients to the superlist
        all_ingredients.extend(ingredients)
        all_ingredients = sorted(all_ingredients,
                                 key=lambda ingredient: ingredient.category_weight,
                                 reverse=True)

    # Write the shopping list
    header = Ingredient.to_table_string()
    with open('shopping_list.txt', 'w') as sl:
        sl.write(f"{header}\n\n")
        sl.writelines((f"{ingredient}\n" for ingredient in all_ingredients))

    # Key = Ingredient.name, Value = url
    urls: dict[str, str] = 'ingredient_url.csv'
    urls = read_ingredient_url_csv(urls)

    # open urls
    open_ingredient_urls(all_ingredients, urls)


if __name__ == "__main__":
    retrieve_ingredients()
