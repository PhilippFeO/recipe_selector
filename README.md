# Recipe Selector #
No "What should I eat for dinner today?" and manually buying ever again! Recipes are selected randomly and a firefox instance will open to buy the necessary ingredients online[^1] – Deciding and grocery shopping in one step!

## How it works
1. Create a firefox profile for grocery shopping only [1].  
    1.1. Insert the path in `main.py`. The variable is the topmost (after the `import` section). <!-- TODO: Background: By using a distings profile, one can keep cookies and login information. The program also won't interfere with your default browser progile you are using on a daily basis. <20-01-2024> -->
2. Place your recipes as `yaml` file in a `recipes/` folder (you may create one). (Disclaimer: This is subject to change in the near future.)  
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
4. The programm will parse the randomly chosen recipes. If it can't find an URL for the specific `Ingredient`, it will ask you to manually add one via the command line. The submitted links are saved and reused separately from the recipe. <!-- TODO: Dadurch muss man bei Änderungen nur an einer Stelle schrauben und nicht in allen Rezepten. Außerdem kann man so schneller Rezepte notieren. <20-01-2024> --> <!-- TODO: Datei generieren, falls sie nicht existiert <20-01-2024> -->
5. After all URLs were collected, Firefox opens the URLs in tabs using your new profile.

---

[1]: If you don't know how to create a new profile, check: https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles?redirectslug=profile-manager-create-and-remove-firefox-profiles&redirectlocale=en-US Keep in mind, that this profile is automatically the default one. So, you have to select your previous profile as standard afterwards. The directory of the profile(s) are also listed on this page. Just copy and paste.

[^1]: At least in Germany it is possible to buy food online at some vendors like Rewe, knuspr and Flink. Especially Rewe is handy, because an App is not necessary and can be done with the desktop browser.
