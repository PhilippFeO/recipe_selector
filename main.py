import sys
import os
import subprocess
from ingredient import Ingredient
from read_ingredients import read_ingredients
from read_csv import read_csv
from open_urls import open_ingredient_urls


def main():
    """
    This function is called via `python3 retrieve_ingredients recipe-1.yaml ...`. Hence, reading and checking `sys.argv`.
    """
    num_recipes = len(sys.argv)

    # Check if at least one file is provided
    if num_recipes <= 1:
        print(
            f"Usage: python {os.path.basename(__file__)} recipe_1.yaml ...")
        sys.exit(1)

    # Initialize a superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []

    # Iterate through command-line arguments starting from the second argument
    for recipe_index in range(1, num_recipes):
        file_path = sys.argv[recipe_index]

        ingredients: list[Ingredient] = read_ingredients(file_path)

        all_ingredients.extend(ingredients)
        all_ingredients = sorted(all_ingredients,
                                 key=lambda ingredient: ingredient.category_weight,
                                 reverse=True)

    # Write the shopping list
    shopping_list_file = 'shopping_list.txt'
    header = Ingredient.to_table_string()
    with open(shopping_list_file, 'w') as slf:
        slf.write(f"{header}\n\n")
        slf.writelines((f"{ingredient}\n" for ingredient in all_ingredients))

    # Open shopping list in $EDITOR to modify it
    # (not all ingredients may be necessary)
    editor = os.environ['EDITOR']
    subprocess.run([editor, shopping_list_file])
    # Without creating 'shopping_list_file' beforehand
    # (but has to be saved manually by ':w shopping_list.txt' which is tideous)
    # ing_tmp = '\n'.join((f"{Ingredient}" for Ingredient in all_ingredients))
    # subprocess.run([editor], input=ing_tmp.encode())

    # Filter final ingredients (second column in 'shopping_list_file')
    # Dont hardcode column number, otherwise changes have to be adapted here again => annoying
    awk_output: str = subprocess.run(
        ['awk', '-F', '   ', f'{{print ${Ingredient._name_col_num}}}', shopping_list_file],
        capture_output=True,
        text=True)
    # Firt two entries are "Name" and "" due to header
    # awk adds '\n', hence there is an empty string entry on the last index
    # I dont know why awk does it and I dont care
    final_ingredients: list[str] = awk_output.stdout.split('\n')[2:-1]

    # Key = Ingredient.name, Value = url
    urls_file = 'res/ingredient_url.csv'
    urls: dict[str, str] = read_csv(urls_file, to_int=False)

    open_ingredient_urls(final_ingredients, urls)


if __name__ == "__main__":
    main()
