import sys
from read_csv import read_csv


class Ingredient:
    field_names = ['?', 'Name', 'Menge', 'Kategorie', 'Gericht']
    # Dont hardcode column number of "Name" because this number is used to filter for the ingredients with awk (s. ./main.py)
    _name_col_num = field_names.index('Name') + 1
    _padding = 15
    _space_column_width = 3
    _category_weights: dict[str, int] = None
    _category_weights_file: str = 'res/category_weights.csv'
    _icu: dict[str, str, str] = None  # i=ingredient, c=category, u=url
    _icu_file: str = 'res/ingredient_category_url.csv'

    def __init__(self, name, quantity, category, url='HIER KÖNNTE IHRE URL STEHEN', optional=False, meal=''):
        self.name = name
        self.quantity = str(quantity)
        self.category = ''
        self.url = ''
        self.optional = optional
        self.meal = meal
        # Fill self.{category, url}
        if Ingredient._icu is None:
            Ingredient._icu = read_csv(Ingredient._icu_file, to_int=False)
        try:
            self.category = Ingredient._icu[self.name][0]
            self.url = Ingredient._icu[self.name][1]
        except KeyError:
            print(f'No {self.category} in {Ingredient._icu_file}')
            print(f'\tField {self.name}.category left empty')
            print(f'\tField {self.name}.url left empty')
        # Assign category weight accoirding to order in supermarket (=> walk from
        # category to category to be efficient).
        # This key is is used for sorting the ingredients when generating the shopping list.
        # Maybe a category i{}s missing, then weight defaults to 0 and has to be added manually.
        if Ingredient._category_weights is None:
            Ingredient._category_weights = read_csv(Ingredient._category_weights_file, to_int=True)
        # Without self.category set, quering for the weight doesn't make sense
        if self.category and self.url:
            try:
                self.category_weight = Ingredient._category_weights[self.category]
            except KeyError:
                self.category_weight = 0
                # Print information about missung category
                # TODO: accomplish this via logging <23-12-2023>
                # s = f"Key\n\t{self.category.lower()}\t({self.name})\nnot found in\n"
                # cw_dict = '\n\t'.join(f"{k}: {v}"
                #                       for k, v in self._category_weights.items())
                # print('\t'.join((s, cw_dict)), file=sys.stderr)
                print(f'{self.category} not found in {Ingredient._category_weights_file}')

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
