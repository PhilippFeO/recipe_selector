import sys
import os
import subprocess
from ingredient import Ingredient
from build_ingredients import build_ingredients
from handle_ing_miss_url import handle_ing_miss_cu
from archive_contents import archive_contents
import logging

firefox_profile_path = os.path.expanduser('~/.mozilla/firefox/5mud7ety.Rewe')


logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s: %(asctime)s] %(message)s',
                    datefmt=' %H:%M:%S')


def main():
    """
    This function is called via `python3 main.py recipe-1.yaml ...`. Hence, reading and checking `sys.argv`.
    """
    sys.argv = ['main.py', 'Testgericht.yaml']
    num_recipes = len(sys.argv)

    # Check if at least one file is provided
    if num_recipes <= 1:
        print(
            f"Usage: python {os.path.basename(__file__)} recipe_1.yaml ...")
        sys.exit(1)

    # i=ingredient, c=category, u=url
    # TODO: csv files may contain error/bad formatted entries (ie. no int were int is ecpected); Check for consistency <05-01-2024>
    icu_file: str = 'res/ingredient_category_url.csv'

    # Superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []
    all_ings_missing_cu: list[Ingredient] = []
    header = Ingredient.to_table_string()
    hline = '\n--------------------------------------------------------------------\n'
    header = header + hline
    shopping_list_str = []

    def collect_ingredients_helper(recipe_file):
        # `valid_ingredients` support `category` and `url`
        # `ings_missing_cu` miss `[c]ategory` and `[u]rl`
        valid_ingredients, ings_missing_cu = build_ingredients(recipe_file, icu_file)
        all_ings_missing_cu.extend(ings_missing_cu)
        return sorted(valid_ingredients + ings_missing_cu,
                      key=lambda ingredient: ingredient.name)

    # Iterate through command-line arguments starting from the second argument
    # TODO: As exercise: parallelize reading/parsing the recipe.yaml <05-01-2024>
    shopping_list_str.append(f'{header}')
    for recipe_file in sys.argv[1:]:
        all_ingredients.extend(collect_ingredients_helper(recipe_file))
    shopping_list_str.append('\n'.join((f"{ingredient}" for ingredient in all_ingredients)) +
                             '\n' * 3)

    dir = 'misc'
    directory = os.fsencode(dir)
    # I want to add a destinct heading for each file in dir misc.
    # Iterating over `sys.argv[1:] + misc_files` would only be possibe with various if-statements
    # because the CLI provided files don't get a "filename" heading like `misc_files` do.
    # To many if-statements affect readability, hence two for loops and helpfer function.
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if '.gitignore' in filename:
            continue
        file_stem = filename.split('.')[0]
        misc_ingredients = collect_ingredients_helper(f'{dir}/{filename}')
        all_ingredients.extend(misc_ingredients)
        shopping_list_str.append(f'{file_stem}:\n' +
                                 f'{header}' +
                                 '\n'.join((f"{ingredient}" for ingredient in misc_ingredients)) +
                                 '\n' * 3)

    # Write the shopping list
    shopping_list_file = 'shopping_list.txt'
    with open(shopping_list_file, 'w') as slf:
        for partial_shopping_list in shopping_list_str:
            slf.write(partial_shopping_list)

    # Open shopping list in $EDITOR to modify it
    # (some ingredients may already be in stock, like salt)
    editor = os.environ['EDITOR']
    # TODO: Set cursor on Position (3,1) if vi, vim, nvim <10-02-2024>
    subprocess.run([editor, shopping_list_file])

    # Filter final ingredients for `name` and `quantity`
    # Dont hardcode column number, otherwise changes have to be adapted here again => annoying
    # Keep `name` column and `quantity` column (the following one)
    # Insert `•` as separator
    awk_output: str = subprocess.run(
        ['awk', '-F', ' {2,}', f'{{print ${Ingredient._name_col_num}, "•", ${Ingredient._name_col_num + 1}}}', shopping_list_file],
        capture_output=True,
        text=True)
    # Firt two entries are "Name" and "" (empty line) due to header
    # awk adds '\n', hence there is an empty string entry on the last index
    # I dont know why awk does it and I dont care
    # list[str]!!! The edited table was splitted above and 'final_ingerdients' contains the names of the ingredients, not the objects!
    # TODO: Consistency checks for the remaining lines <17-01-2024>
    final_ingredient_names: list[str] = awk_output.stdout.split('\n')[:-1]
    final_ingredient_names = [e for e in final_ingredient_names if e not in {' • ', 'Name • Menge'}]
    # Transform list of "name • quantity"-strings into list of tuples with (name, quantity) entries
    ing_quant = ((i.strip(), q.strip()) for i, q in (fin.split('•') for fin in final_ingredient_names))
    # Filter `all_ingredients` to keep described ones by `final_ingredient_names`
    #   "described" because `final_ingredient_names` holds only strings (and not `Ingredient`s)
    final_ingredients: list[Ingredient] = []
    for i, q in ing_quant:
        for ingredient in all_ingredients:
            # Enrties in shopping list are cut after 15 chars, so comparison is based on these
            if ingredient.name[:Ingredient._padding] == i and ingredient.quantity == q:
                final_ingredients.append(ingredient)
                break
    # TODO: When printing give user the chance to reedit list <18-01-2024>
    print("\nFinal shopping list:")
    print(f'{header}\n', *final_ingredients, sep='\n', end='\n')

    # Archive shopping list and recipes
    archive_contents(shopping_list_file, sys.argv[1:])

    # Copy shopping_list_file to dir 'selection'
    # hard link recipes
    # TODO: Hard link PDFs <31-01-2024>

    urls = handle_ing_miss_cu(all_ings_missing_cu,
                              final_ingredients,
                              icu_file)

    # Open firefox with specific profile
    # subpress warnings
    firefox = f"firefox --profile {firefox_profile_path}"
    # subprocess.run([editor, shopping_list_file])
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
