import yaml
import os
import logging
from ingredient import Ingredient
from read_csv import read_csv


def build_ingredients(recipe_file: str, icu_file: str) -> tuple[list[Ingredient], list[Ingredient]]:
    """
    Builds the ingredient list of a recipe by parsing the yaml file and adding
    the information from the corresponding CSV files, namely `category` and `url`.

    The function will return two lists, the first holding `Ingredient`s with valid `category` and `url` attributes, the latter with predefined ones.
    This necessary to ask the user for completing the data.

    I know, there are other methods to store objects but Text (in comparison to binary) gives the user the opportunity to edit the data.
    Additionally, this surely becomes necessary because nobody can guarantee that an URL will stay valid. The vendor might change it.
    """
    recipe_data = None
    with open(recipe_file, 'r') as file:
        recipe_data = yaml.safe_load(file)

    recipe_ingredients: list[Ingredient] = []
    # User will be asked to provide `[c]ategory` and `[u]rl`
    ings_missing_cu: list[Ingredient] = []

    # Build ingredients
    # get() returns list of dicts resembling an ingredient as defined in the corresponding yaml file
    recipe_name = recipe_data.get('recipe', [])[0]['name']
    ingredients: list[dict[str, str]] = recipe_data.get("ingredients", [])
    icu_dict: dict[str, tuple[str, str]] = {}
    try:
        icu_dict = read_csv(icu_file)
    except FileNotFoundError:
        # File will be created in the following, s. handle_ing_miss_url.py
        pass
    for ingredient in ingredients:
        # Retrive information from CSV files ('category', 'url' and 'category_weight')
        ingredient_name = ingredient['name']
        # Check for 'KeyError' in all CSV files
        # DONE: KeyError might occur <05-01-2024>
        try:
            # If URL is missing, it will be added later by the user
            category = icu_dict[ingredient_name][0]
            url = icu_dict[ingredient_name][1]
        except KeyError:
            logging.info(f'Ingredient "{ingredient_name}" missing in "{icu_file}". Default value for <category> will be used.')
            ings_missing_cu.append(
                Ingredient(**ingredient,
                           meal=recipe_name))
            continue
        recipe_ingredients.append(
            Ingredient(**ingredient,  # Only holds `name` and `quantity`
                       category=category,
                       url=url,
                       meal=recipe_name))
    return recipe_ingredients, ings_missing_cu


if __name__ == "__main__":
    file_path = "recipes/Testgericht.yaml"
    # i=ingredient, c=category, u=url
    icu_file = 'res/ingredient_category_url.csv'
    aicu_dict: dict[str, tuple[str, str]] = read_csv(icu_file)
    ingredients = build_ingredients(file_path, aicu_dict)

    for i in ingredients:
        print(i)
