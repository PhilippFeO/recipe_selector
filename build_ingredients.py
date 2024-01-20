import yaml
import os
from ingredient import Ingredient
from read_csv import read_csv

# TODO: Remove hardcoded file path <05-01-2024>
#   Idea: Closure, ie. a function 'read_all_csvs' reads the csvs and returns the 'build_ingredient' function
icu_file = 'res/ingredient_category_url.csv'
# category_weights_file = 'res/category_weights.csv'


def build_ingredients_from_csv(file_path: str,
                               icu_dict: dict[str, tuple[str, str]]) -> tuple[list[Ingredient], list[Ingredient]]:
    """
    Builds the ingredient list of a recipe by parsing the yaml file and adding
    the information from the corresponding CSV files, namely `category` and `url`.

    The function will return two lists, the first holding `Ingredient`s with valid `category` and `url` attributes, the latter with predefined ones.
    This necessary to ask the user for completing the data.

    I know, there are other methods to store objects but Text (in comparison to binary) gives the user the opportunity to edit the data.
    Additionally, this surely becomes necessary because nobody can guarantee that an URL will stay valid. The vendor might change it.
    """
    recipe_name = os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ')
    recipe_data = None
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)

    recipe_ingredients: list[Ingredient] = []
    ings_missing_cu = []

    # Build ingredients
    # get() returns list of dicts resembling an ingredient as defined in the corresponding yaml file
    ingredients: list[dict[str, str]] = recipe_data.get("ingredients", [])
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
            print(
                f'Ingredient "{ingredient_name}" missing in "{icu_file}". Default value for <category> will be used.')
            ings_missing_cu.append(
                Ingredient(**ingredient,
                           meal=recipe_name))
            continue
        recipe_ingredients.append(
            Ingredient(**ingredient,  # Only holds `name` and `quantity`
                       category=category,
                       url=url,
                       # basename provides file name, splittext separates name and extension, [0] uses plain file name
                       # TODO: Add 'recipe: RECIPENAME' key to every recipe to avoid this ugly line of code <05-01-2024>
                       meal=recipe_name))
    return recipe_ingredients, ings_missing_cu


if __name__ == "__main__":
    file_path = "recipes/Testgericht.yml"
    # i=ingredient, c=category, u=url
    icu_dict: dict[str, tuple[str, str]] = read_csv(icu_file, to_int=False)
    # category_weights: dict[str, int] = read_csv(category_weights_file, to_int=True)
    ingredients = build_ingredients_from_csv(file_path, icu_dict)

    for i in ingredients:
        print(i)
