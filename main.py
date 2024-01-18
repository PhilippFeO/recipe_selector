import sys
from typing import Generator
import os
import subprocess
from ingredient import Ingredient
from read_ingredients import build_ingredients
from read_csv import read_csv


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
    # Keep "name" column and "quantity" column (the following one)
    # Insert "•" as separator
    awk_output: str = subprocess.run(
        ['awk', '-F', ' {2,}', f'{{print ${Ingredient._name_col_num}, "•", ${Ingredient._name_col_num + 1}}}', shopping_list_file],
        capture_output=True,
        text=True)
    # Firt two entries are "Name" and "" (empty line) due to header
    # awk adds '\n', hence there is an empty string entry on the last index
    # I dont know why awk does it and I dont care
    # list[str]!!! The edited table was splitted above and 'final_ingerdients' contains the names of the ingredients, not the objects!
    # TODO: User might delete shopping list completly => [2:-1] will return an empty list <05-01-2024>
    # TODO: Consistency checks for the remaining lines <17-01-2024>
    final_ingredient_names: list[str] = awk_output.stdout.split('\n')[2:-1]
    # Transform list of "name • quantity" into list of tuples with (name, quantity) entries
    ing_quant = ((i.strip(), q.strip()) for i, q in (fin.split('•') for fin in final_ingredient_names))
    # Filter `all_ingredients` to keep described by `final_ingredient_names`
    #   "described" because `final_ingredient_names` holds only strings
    final_ingredients: list[Ingredient] = []
    for i, q in ing_quant:
        for ingredient in all_ingredients:
            if ingredient.name == i and ingredient.quantity == q:
                final_ingredients.append(ingredient)
                break
    # TODO: Use logging and/or print output for user <18-01-2024>
    # TODO: When printing give user the chance to reedit list <18-01-2024>
    print()
    print("Final shopping list:")
    print(f'{header}\n')
    print(*final_ingredients, sep='\n')
    print()

    # Check for missing URLs
    ing_miss_url = []
    for ingredient in final_ingredients:
        ing_name = ingredient.name
        try:
            ingredient.url = icu_dict[ing_name][1]
        except KeyError:
            ing_miss_url.append(ingredient)

    # Query user to add missing URLs for ingredients
    if ing_miss_url:
        while True:
            print("Do you want to instert missing links for the following ingredients?\n")
            ing_names_miss_url: Generator[str, None, None] = (f'{ing.name}\n' for ing in ing_miss_url)
            join_str = '\t - '
            bullet_list_ing_miss_url: str = join_str + join_str.join(ing_names_miss_url)
            print(f'{bullet_list_ing_miss_url}')
            user_input: str = input("yes/no: ").lower()
            if user_input in {'yes', 'y'}:
                # Ask user for URL of every ingredient, append collected URLs to `icu_file`
                for ing in ing_miss_url:
                    ing.url = input(f'URL of "{ing.name}": ')
                    # Default value if user entered now URL
                    # TODO: Let user reedit list if URLs are still missing <18-01-2024>
                    if ing.url == '':
                        ing.url = '--url--'
                # Now, all missing URLs were completed
                icu_entries = '\n'.join((f'{ing.name},{ing.category},{ing.url}' for ing in ing_miss_url)) + '\n'
                with open(icu_file, 'a') as f:
                    f.write(icu_entries)
                break
            elif user_input in {'no', 'n'}:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    # Open firefox with specific profile
    # subpress warnings
    urls = tuple(ing.url for ing in final_ingredients)
    print()
    print(*urls, sep='\n')
    firefox = "firefox --profile /home/philipp/.mozilla/firefox/5mud7ety.Rewe"
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
