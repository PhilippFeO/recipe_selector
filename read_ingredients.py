import yaml
import os
from ingredient import Ingredient
from read_csv import read_csv

# TODO: Remove hardcoded file path <05-01-2024>
#   Idea: Closure, ie. a function 'read_all_csvs' reads the csvs and returns the 'build_ingredient' function
icu_file = 'res/ingredient_category_url.csv'
category_weights_file = 'res/category_weights.csv'
default_category = '-- fehlt --'


def build_ingredients(file_path: str,
                      icu_dict: dict[str, tuple[str, str]],
                      category_weights: dict[str, int]):
    """
    Builds the ingredient list of a recipe by parsing the yaml file and adding
    the information from the corresponding CSV files, namely `category`, `category_weight`
    and `url`.
    """
    recipe_data = None
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)

    recipe_ingredients: list[Ingredient] = []

    # Build ingredients
    # get() returns list of dicts resembling an ingredient as defined in the corresponding yaml file
    ingredients: list[dict[str, str]] = recipe_data.get("ingredients", [])
    for ingredient in ingredients:
        # Retrive information from CSV files ('category', 'url' and 'category_weight')
        ingredient_name = ingredient['name']
        # Check for 'KeyError' in all CSV files
        # DONE: KeyError might occur <05-01-2024>
        try:
            category = icu_dict[ingredient_name][0]
        except KeyError:
            print(
                f'Ingredient "{ingredient_name}" missing in "{icu_file}". Default value for <category> will be used.')
            category = default_category
            c_weight = 0  # Set here, because 'category_weights' won't be queried
        # No ingredient => no category => no category_weight
        # => Proceed if 'category' is a valid key
        if category != default_category:
            try:
                c_weight = category_weights[category]
            except KeyError:
                print(
                    f'Category "{category}" missing in "{category_weights_file}". Default value for <category_weight> will be used.')
                c_weight = 0
        # Build ingredient and insert into list
        recipe_ingredients.append(
            Ingredient(**ingredient,
                       category=category,
                       category_weight=c_weight,
                       # basename provides file name, splittext separates name and extension, [0] uses plain file name
                       # TODO: Add 'recipe: RECIPENAME' key to every recipe to avoid this ugly line of code <05-01-2024>
                       meal=os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ')))
    return recipe_ingredients


if __name__ == "__main__":
    file_path = "recipes/Testgericht.yml"
    # i=ingredient, c=category, u=url
    icu_dict: dict[str, tuple[str, str]] = read_csv(icu_file, to_int=False)
    category_weights: dict[str, int] = read_csv(category_weights_file, to_int=True)
    ingredients = build_ingredients(file_path, icu_dict, category_weights)

    for i in ingredients:
        print(i)
