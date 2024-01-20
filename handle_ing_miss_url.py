from ingredient import Ingredient
from typing import Generator


def query_for_url(ings_miss_cu: list[Ingredient],
                  icu_file: str):
    """
    Ask user for URL of every `Ingredient` in `ing_miss_url`, append collected URLs to `icu_file` ([i]ngredient, [c]ategory, [u]rl).
    """
    for ing in ings_miss_cu:
        c = input(f'\nCategory of "{ing.name}": ')
        # Only change `category` if there was a "real" input ("real" == "not empty")
        # Otherwise, `category` keeps the default value set in the constructor
        if c != '':
            ing.category = c
        # Same with url
        u = input(f'URL of "{ing.name}": ')
        if u != '':
            ing.url = u
    # Now, all missing `category` and `url` were completed => append to CSV file
    icu_entries = '\n'.join((f'{ing.name},{ing.category},{ing.url}' for ing in ings_miss_cu)) + '\n'
    with open(icu_file, 'a') as f:
        f.write(icu_entries)


def handle_ing_miss_cu(ings_miss_cu: list[Ingredient],
                       final_ingredients: list[Ingredient],
                       icu_file: str) -> list[str]:
    """
    Initial query to give the opportunity to add `category` and `url` to the `Ingredient`s in `ings_miss_cu`.
    The `Ingredient`s are listed before user input is parsed. After all Categories and URLs were collected, they will be appended to the `icu_file` ([i]ngredient, [c]ategory, [u]rl).

    The list of **all** URLs is returned.
    """
    if ings_miss_cu:
        while True:
            print("Do you want to add the missing `category` and `url` for the following ingredients?\n")
            ing_names_miss_url: Generator[str, None, None] = (f'{ing.name}\n' for ing in ings_miss_cu)
            join_str = '\t - '
            bullet_list_ing_miss_url: str = join_str + join_str.join(ing_names_miss_url)
            print(f'{bullet_list_ing_miss_url}')
            user_input: str = input("yes/no: ").lower()
            if user_input in {'yes', 'y'}:
                query_for_url(ings_miss_cu,
                              icu_file)
                break
            elif user_input in {'no', 'n'}:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    # `final_ingredients` shares `Ingerdient`s from `valid_ingredients` and `ings_miss_cu` (s. `main.py`), since we are dealing with objects, **references** were passed around.
    urls = tuple(ing.url for ing in final_ingredients)
    return urls
