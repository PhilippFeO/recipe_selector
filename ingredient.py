import yaml


class Ingredient:
    def __init__(self, name, amount, type, optional=False):
        self.name = name
        self.amount = str(amount)
        self.type = type
        self.optional = optional

    def __str__(self):
        optional_str = " (Optional)" if self.optional else ""
        return f"{self.name}: {self.amount} ({self.type}){optional_str}"


def read_ingredients(file_path):
    recipe_data = None
    with open(file_path, 'r') as file:
        recipe_data = yaml.safe_load(file)

    ingredients = recipe_data.get("ingredients", [])
    return [Ingredient(**ingredient) for ingredient in ingredients]


if __name__ == "__main__":
    file_path = "recipes/bowl.yaml"
    ingredients = read_ingredients(file_path)

    for i in ingredients:
        print(i)

# class Recipe:
#     def __init__(self, title, servings, ingredients, instructions):
#         self.title = title
#         self.servings = servings
#         self.ingredients = [Ingredient(**ingredient)
#                             for ingredient in ingredients]
#         self.instructions = instructions
#
#     def __str__(self):
#         recipe_str = f"Recipe: {self.title}\nServings: {self.servings}\n\nIngredients:"
#         for ingredient in self.ingredients:
#             recipe_str += f"\n- {ingredient}"
#
#         recipe_str += "\n\nInstructions:"
#         for step in self.instructions:
#             step_number = step.get("step", "N/A")
#             description = step.get("description", "N/A")
#             recipe_str += f"\n{step_number}. {description}"
#
#         return recipe_str
#
#
# def read_recipe(file_path):
#     with open(file_path, 'r') as file:
#         recipe_data = yaml.safe_load(file)
#     return Recipe(**recipe_data['recipe'])
