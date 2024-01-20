from ingredient import Ingredient
from typing import Generator


def retrieve_ing_miss_url(final_ingredients: list[Ingredient],
                          icu_dict: dict[str, tuple[str, str]]) -> list[Ingredient]:
    """
    Filters the list `final_ingredients` for `Ingredient`s with no corresponding URL in the `icu_dict` ([i]ngredient, [c]ategory, [u]rl).
    """
    # Check for missing URLs
    ing_miss_url = []
    for ingredient in final_ingredients:
        ing_name = ingredient.name
        try:
            ingredient.url = icu_dict[ing_name][1]
        except KeyError:
            ing_miss_url.append(ingredient)
    return ing_miss_url


def query_for_url(ings_miss_cu: list[Ingredient],
                  icu_file: str):
    """
    Ask user for URL of every `Ingredient` in `ing_miss_url`, append collected URLs to `icu_file` ([i]ngredient, [c]ategory, [u]rl).
    """
    for ing in ings_miss_cu:
        c = input(f'Category of "{ing.name}": ')
        # Only change `category` if there was a "real" input ("real" == "not empty")
        # Otherwise, `category` keeps the default value set in the constructor
        if c != '':
            ing.category = c
        # Same with url
        u = input(f'URL of "{ing.name}": ')
        if u != '':
            ing.url = u
    # Now, all missing URLs were completed
    icu_entries = '\n'.join((f'{ing.name},{ing.category},{ing.url}' for ing in ings_miss_cu)) + '\n'
    with open(icu_file, 'a') as f:
        f.write(icu_entries)


def handle_ing_miss_cu(ings_miss_cu: list[Ingredient],
                       final_ingredients: list[Ingredient],
                       icu_file: str) -> list[str]:
    """
    Initial query to give the opportunity to add URLs to the `Ingredient`s in `ing_miss_url`.
    The `Ingredient`s are listed before user input is parsed. After all URLs were collected,
    they will be appended to the `icu_file` ([i]ngredient, [c]ategory, [u]rl)self.

    The list of the missing URLs is returned.
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
    # In `retrieve_ing_miss_url()` the `Ingerdient`s are appended to `ing_miss_url`, ie. not removed from `final_ingredients` and **not** copied.
    # So, `ing_miss_url` and `final_ingredients` share `Ingredient`s. In `query_for_url()` the
    # `url` attribute is set and because the `Ingerdient` is present in both list, `final_ingredients` also the URL or no `Ingredient`s without URL anymore.
    urls = tuple(ing.url for ing in final_ingredients)
    return urls
