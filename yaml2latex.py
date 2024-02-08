import yaml
import argparse
import subprocess
import logging
from pathlib import Path
from ingredient import Ingredient


class Recipe:
    def __init__(self, recipe_name, ingredients, preparation):
        self.recipe_name = recipe_name
        self.ingredients: list[Ingredient] = [Ingredient(**ingredient)
                                              for ingredient in ingredients]
        self.preparation: list[str] = preparation

    def to_latex(self):
        # TODO: Write strings to pipe, read form pipe in latex file <06-02-2024>
        res_dir = 'res'
        with open(f'{res_dir}/title.tex', 'w') as recipe_name_file:
            recipe_name_file.write(self.recipe_name)
        with open(f'{res_dir}/ingredients.tex', 'w') as ingredients_file:
            ingredients_file.writelines((f'\\item {ing.quantity} {ing.name}\n' for ing in self.ingredients))
        with open(f'{res_dir}/preparation.tex', 'w') as preparation_file:
            preparation_file.writelines((f'\\item {step[3:]}\n' for step in self.preparation))


def read_recipe(file_path):
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)
    return Recipe(recipe_data['recipe'][0]['name'], recipe_data['ingredients'], recipe_data['preparation'])


if __name__ == '__main__':
    p = argparse.ArgumentParser("isolate_shape")
    p = argparse.ArgumentParser(__name__)
    p.add_argument("recipe_yaml",
                   help="One or more yaml files containing a recipe.",
                   type=str,
                   nargs='+',
                   default=["recipes/Testgericht.yaml"])
    args = p.parse_args()

    for recipe_file in args.recipe_yaml:
        recipe: Recipe = read_recipe(recipe_file)
        recipe.to_latex()
        # Compile recipe before moving to next
        cp: subprocess.CompletedProcess = subprocess.run(['./compile_recipe.sh', 'recipe-template.tex'],
                                                         # stdout=subprocess.DEVNULL,
                                                         # stderr=subprocess.DEVNULL
                                                         )
        if cp.returncode != 0:
            logging.error(f'Compilation of "{recipe_file}" failed.')
        else:
            basename = Path(recipe_file).stem
            subprocess.run(['mv', 'res/out/recipe-template.pdf', f'recipes/pdf/{basename}.pdf'])
