import yaml
import argparse
import subprocess
import logging
from pathlib import Path
from ingredient import Ingredient
from itertools import zip_longest


class Recipe:
    def __init__(self, recipe_name, ingredients, preparation):
        self.recipe_name = recipe_name
        self.ingredients: list[Ingredient] = [Ingredient(**ingredient)
                                              for ingredient in ingredients]
        self.preparation: list[str] = [step
                                       .replace('„', '"`')
                                       .replace('“', '"\'')
                                       .replace('&', '\\&') for step in preparation]

    def to_latex(self):
        # TODO: Write strings to pipe, read form pipe in latex file <06-02-2024>
        res_dir = 'res'
        # Recipe title
        with open(f'{res_dir}/title.tex', 'w') as recipe_name_file:
            recipe_name_file.write(self.recipe_name)
        # Preparation
        with open(f'{res_dir}/preparation.tex', 'w') as preparation_file:
            # Each step starts with '\d{1,2}.\s', ie 3-4 chars
            # TODO: Adjust slice according to above comment <13-02-2024, Philipp Rost>
            #   Idea: 'preparation' object containing number and instruction separately
            # Works because Latex collapses multiple spaces (after `\item`) into one
            preparation_file.writelines((f'\\item {step[3:]}\n' for step in self.preparation))

        # Ingredients
        table_body = ''

        # Make optional ingredients gray
        def color_ingredient(ing: Ingredient) -> str:
            """ Dye optional ingredients gray. """
            if ing and ing.optional:
                s = f'\\textcolor{{gray}}{{- {ing.quantity} {ing.name}}}'
            elif ing:
                s = f'- {ing.quantity} {ing.name}'
            else:
                s = ''
            return s

        # `sorted()` sets False before True
        ings_sorted = sorted(self.ingredients, key=lambda ing: ing.optional)
        # I prefere having optional (gray) ingredients in the right column, ie. I have to split
        # `ings_sorted` in half and align both sublists as columns or do some index mangling.
        # In case of odd number of ingredients, `fillvalue` enhances the second shorter iterable
        middle_idx = len(ings_sorted) // 2
        for ing1, ing2 in zip_longest(ings_sorted[:middle_idx],
                                      ings_sorted[middle_idx:],
                                      fillvalue=None):
            ing1_as_field, ing2_as_field = color_ingredient(ing1), color_ingredient(ing2)
            table_row = f'{ing1_as_field} & {ing2_as_field}\\\\\n'
            table_body += table_row
        with open(f'{res_dir}/ingredients.tex', 'w') as ingredients_file:
            ingredients_file.writelines(table_body)


def read_recipe(file_path):
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)
    return Recipe(recipe_data['recipe'][0]['name'], recipe_data['ingredients'], recipe_data['preparation'])


if __name__ == '__main__':
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
        cp: subprocess.CompletedProcess = subprocess.run(['./compile_recipe.sh', 'template.tex'],
                                                         # stdout=subprocess.DEVNULL,
                                                         # stderr=subprocess.DEVNULL
                                                         )
        if cp.returncode != 0:
            logging.error(f'Compilation of "{recipe_file}" failed.')
        else:
            basename = Path(recipe_file).stem
            subprocess.run(['mkdir', '-p', 'recipes/pdf/'])
            subprocess.run(['mv', 'res/out/template.pdf', f'recipes/pdf/{basename}.pdf'])
