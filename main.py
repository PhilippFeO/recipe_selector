import sys
import os
import subprocess
from ingredient import Ingredient
from read_ingredients import build_ingredients
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

    # i=ingredient, c=category, u=url
    # TODO: csv files may contain error/bad formatted entries (ie. no int were int is ecpected); Check for consistency <05-01-2024>
    icu_file: str = 'res/ingredient_category_url.csv'
    icu_dict: dict[str, tuple[str, str]] = read_csv(icu_file, to_int=False)
    category_weights: dict[str, int] = read_csv('res/category_weights.csv', to_int=True)

    # Superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []

    # Iterate through command-line arguments starting from the second argument
    # TODO: As exercise: parallelize reading from file <05-01-2024>
    for recipe_index in range(1, num_recipes):
        file_path = sys.argv[recipe_index]

        ingredients: list[Ingredient] = build_ingredients(file_path, icu_dict, category_weights)

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
    # (some ingredients may already be in stock)
    editor = os.environ['EDITOR']
    subprocess.run([editor, shopping_list_file])

    # Filter final ingredients (second column in 'shopping_list_file')
    # Dont hardcode column number, otherwise changes have to be adapted here again => annoying
    awk_output: str = subprocess.run(
        ['awk', '-F', '   ', f'{{print ${Ingredient._name_col_num}}}', shopping_list_file],
        capture_output=True,
        text=True)
    # Firt two entries are "Name" and "" (empty line) due to header
    # awk adds '\n', hence there is an empty string entry on the last index
    # I dont know why awk does it and I dont care
    # list[str]!!! The edited table was splitted above and 'final_ingerdients' contains the names of the ingredients, not the objects!
    # TODO: User might delete shopping list completly => [2:-1] will return an empty list <05-01-2024>
    # TODO: Consistency checks for the remaining lines <17-01-2024>
    final_ingredient_names: list[str] = awk_output.stdout.split('\n')[2:-1]

    # Query user to add missing URLs for ingredients
    # Will insert CSV-stump (`imu`) and open $EDITOR
    ing_missing_url: list[str] = open_ingredient_urls(final_ingredient_names, icu_dict)
    if ing_missing_url:
        while True:
            print("Do you want to instert missing links for the followin ingredients?\n")
            join_str = '\t - '
            list_ing_missing_url = join_str + join_str.join(ing_missing_url)
            print(f'{list_ing_missing_url}\n')
            user_input: str = input("yes/no: ").lower()
            if user_input in {'yes', 'y'}:
                join_str = ',DEFAULT,URL'
                imu = join_str.join(ing_missing_url)
                imu = f'{imu}{join_str}\n'
                with open(icu_file, 'a') as icu_file:
                    icu_file.write(imu)
                subprocess.run([editor, icu_file])
                break
            elif user_input in {'no', 'n'}:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()
