import sys
from read_csv import read_csv


class Ingredient:
    field_names = ['?', 'Name', 'Menge', 'Kategorie', 'Gericht']
    # Dont hardcode column number of "Name" because this number is used to filter for the ingredients with awk (s. ./main.py)
    _name_col_num = field_names.index('Name') + 1
    _padding = 15
    _space_column_width = 3
    _category_weights = None

    def __init__(self, name, quantity, category, url='HIER KÖNNTE IHRE URL STEHEN', optional=False, meal=''):
        self.name = name
        self.quantity = str(quantity)
        self.category = category
        self.url = url
        self.optional = optional
        self.meal = meal
        # Assign category weight accoirding to order in supermarket (=> walk from
        # category to category to be efficient).
        # This key is is used for sorting the ingredients when generating the shopping list.
        # Maybe a category i{}s missing, then weight defaults to 0 and has to be added manually.
        Ingredient._category_weights = read_csv('res/category_weights.csv', to_int=True)
        try:
            self.category_weight = Ingredient._category_weights[category.lower()]
        except KeyError:
            self.category_weight = 0
            # Print information about missung category
            # TODO: accomplish this via logging <23-12-2023>
            s = f"Key\n\t{self.category.lower()}\t({self.name})\nnot found in\n"
            cw_dict = '\n\t'.join(f"{k}: {v}"
                                  for k, v in self._category_weights.items())
            print('\t'.join((s, cw_dict)), file=sys.stderr)

    def __str__(self):
        return Ingredient.to_table_string([self.optional,
                                           self.name,
                                           self.quantity,
                                           self.category,
                                           self.meal])

    # Also used for crafting a header for the table, hence class method and first argument as list
    # (The field names are provided as list, attributes follow)
    # Padding, to have a small neat table
    @classmethod
    def to_table_string(cls, attributes: list = field_names):
        """
        Format elements (field names, ingredient) as string for shopping list.
        """
        optional, name, quantity, category, meal = attributes
        # Cap at _padding, no matter what (keep in mind when comosing a recipe)
        pad = Ingredient._padding
        scw = Ingredient._space_column_width
        s = '?' if optional == '?' else '1' if optional else '.'
        s = (' ' * scw).join((s, *(f"{attr[:pad]:<{pad}}"
                                   for attr in [name,
                                                quantity,
                                                category])))
        s = ' '.join((s, meal))
        return s


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
