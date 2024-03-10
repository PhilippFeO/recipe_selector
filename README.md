This repository is depracted in favor of [grocery-shopper](https://github.com/PhilippFeO/grocery-shopper). It will be deleted in the middle distant future. If you like the repository, consider switching. You can keep your recipes and the `res/ingredient_category_url.csv` file. If any questions arise, feel free to open an issue!

# Recipe Selector #
No "What should I eat for dinner today?" and manually buying ever again! Recipes are selected randomly and a firefox instance will open to buy the necessary ingredients online[^1] – Deciding and grocery shopping in one step!

## Installation
Clone the git repository (wherever you like):
```sh
git clone https://github.com/PhilippFeO/recipe_selector
```
make [`select_recipes.sh`](./select_recipes.sh) executable via `chmod +x select_recipes.sh` and go.

## How it works
1. Create a firefox profile for grocery shopping only [1].
    1.1. Insert the path in `main.py`. The variable is the topmost after the `import` section. (Background: By using a distings profile, one can keep cookies and login information. The program also won't interfere with your default browser profile you are using on a daily basis.)
2. Place your recipes as `yaml` files in a `recipes/` folder (you may create one). (Disclaimer: This is subject to change in the near future.)  
    2.1. Your recipe should have the following structure:
```yaml
ingredients:
    - name: Spaghetti
      quantity: 250g
    - name: Tomato(s)
      quantity: 5
    ...
preparation:
    - 1. Cook the Spaghetti.
    - 2. Produce a Tomatosauce.
    ...
```
3. Start `./select_recipes.sh`
4. The programm will parse the randomly chosen recipes. If it can't find an URL for the specific `Ingredient`, it will ask you to manually add one via the command line. The submitted links are saved and reused separately from the recipe. 
5. After all URLs were collected, Firefox opens the URLs in tabs using your new profile.

### Some thoughts on 4.
It is also possible to provide the URL as a field (`url`) in the `yaml` of the recipe but then we have to provide the URL each time using the `Ingredient`. By having a separate file storing `Ingredient.name` (`.name` since only the string is used in this case) and it's URL, we have one source of truth. This is quite handy if URLs change, because then we have to edit it once and not across each recipe. The combination is saved under `res/ingredient_category_url.csv`. Having plain text/csv and no binary gives us the opportunity to easily make changes afterwards. An additional benefit is that this speeds up creating a new recipe since most `Ingredient`s are already provided with an URL and wo don't have to insert the same information again and again.

## Syntax completion for Neovim
- I have written a source for Neovim, ie. [nvim-cmp](https://github.com/hrsh7th/nvim-cmp) which completes the ingredients. You can find it in my Repos or [here](https://github.com/PhilippFeO/cmp-csv). Having syntax completion provides you from typos, duplication and remembering which `Ingredient` is already with URL available.

---

[1]: If you don't know how to create a new profile, check: https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles?redirectslug=profile-manager-create-and-remove-firefox-profiles&redirectlocale=en-US Keep in mind, that this profile is automatically the default one. So, you have to select your previous profile as standard afterwards. The directory of the profile(s) are also listed on this page. Just copy and paste.

[^1]: At least in Germany it is possible to buy food online at some vendors like Rewe, knuspr and Flink. Especially Rewe is handy, because an App is not necessary and can be done with the desktop browser.
