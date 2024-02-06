import yaml
from ingredient import Ingredient


class Recipe:
    def __init__(self, recipe_name, ingredients, preparation):
        self.recipe_name = recipe_name
        self.ingredients: list[Ingredient] = [Ingredient(**ingredient)
                                              for ingredient in ingredients]
        self.preparation: list[str] = preparation

    def to_latex(self):
        # TODO: Write strings to pipe, read form pipe in latex file <06-02-2024>
        latex_path = './tex'
        with open(f'{latex_path}/title.tex', 'w') as recipe_name_file:
            recipe_name_file.write(self.recipe_name)
        with open(f'{latex_path}/ingredients.tex', 'w') as ingredients_file:
            ingredients_file.writelines((f'\\item {ing.quantity} {ing.name}\n' for ing in self.ingredients))
        with open(f'{latex_path}/preparation.tex', 'w') as preparation_file:
            preparation_file.writelines((f'\\item {step[3:]}\n' for step in self.preparation))


def read_recipe(file_path):
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)
    return Recipe(recipe_data['recipe'][0]['name'], recipe_data['ingredients'], recipe_data['preparation'])


if __name__ == '__main__':
    file_path = 'Testgericht.yaml'
    recipe: Recipe = read_recipe(file_path)
    recipe.to_latex()
