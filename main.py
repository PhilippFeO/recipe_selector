import sys
import os
import subprocess
from ingredient import Ingredient
from build_ingredients import build_ingredients
# from read_csv import read_csv
from handle_ing_miss_url import handle_ing_miss_cu

firefox_profile_path = os.path.expanduser('~/.mozilla/firefox/5mud7ety.Rewe')


def main():
    """
    This function is called via `python3 main.py recipe-1.yaml ...`. Hence, reading and checking `sys.argv`.
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

    # Superlist to store ingredients from all files
    all_valid_ingredients: list[Ingredient] = []

    # Iterate through command-line arguments starting from the second argument
    # TODO: As exercise: parallelize reading/parsing the recipe.yaml <05-01-2024>
    for recipe_index in range(1, num_recipes):
        recipe_file = sys.argv[recipe_index]

        # `valid_ingredients` support `category` and `url`
        # `ings_missing_cu` miss `[c]ategory` and `[u]rl`
        valid_ingredients, ings_missing_cu = build_ingredients(recipe_file, icu_file)

        all_valid_ingredients.extend(valid_ingredients)
        all_valid_ingredients = sorted(all_valid_ingredients,
                                       key=lambda ingredient: ingredient.category,
                                       reverse=True)

    # Write the shopping list
    all_ingredients = valid_ingredients + ings_missing_cu
    shopping_list_file = 'shopping_list.txt'
    header = Ingredient.to_table_string()
    with open(shopping_list_file, 'w') as slf:
        slf.write(f"{header}\n\n")
        slf.writelines((f"{ingredient}\n" for ingredient in all_ingredients))

    # Open shopping list in $EDITOR to modify it
    # (some ingredients may already be in stock, like salt)
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
    # Filter `all_ingredients` to keep described ones by `final_ingredient_names`
    #   "described" because `final_ingredient_names` holds only strings (and not `Ingredient`s)
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

    urls = handle_ing_miss_cu(ings_missing_cu,
                              final_ingredients,
                              icu_file)
    print()
    print(*urls, sep='\n')

    # Open firefox with specific profile
    # subpress warnings
    firefox = f"firefox --profile {firefox_profile_path}"
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
