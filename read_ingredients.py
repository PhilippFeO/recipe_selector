import yaml
import os
from ingredient import Ingredient


def read_ingredients(file_path):
    recipe_data = None
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)

    ingredients = recipe_data.get("ingredients", [])
    # basename provides file name, splittext separates name and extension, [0] uses plain file name
    return [Ingredient(**ingredient, meal=os.path.splitext(os.path.basename(file_path))[0].replace('_', ' '))
            for ingredient in ingredients]


if __name__ == "__main__":
    file_path = "recipes/Spaghetti_mit_Gemüse.yml"
    ingredients = read_ingredients(file_path)

    for i in ingredients:
        print(i)
