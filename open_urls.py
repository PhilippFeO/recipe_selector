import webbrowser


def open_ingredient_urls(ingredient_names: list[str], icu_dict: dict[str, str]):
    firefox_path = "/usr/bin/firefox"
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    # Open browser, ie. landing page to log in
    landing_page = 'www.wikipedia.org'
    webbrowser.get('firefox').open_new(landing_page)

    # Open each URL in Firefox
    for ing_name in ingredient_names:
        try:
            url = icu_dict[ing_name][1]
        except KeyError:
            print(f'Ingredient "{ing_name}" has no url.')
            continue  # No ingredient_name in dict => continue loop
        webbrowser.get('firefox').open_new_tab(url)
