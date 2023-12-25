import webbrowser
from ingredient import Ingredient


def open_ingredient_urls(ingredients: list[Ingredient], urls: dict[str, str]):
    # Update with your Firefox installation path
    firefox_path = "/usr/bin/firefox"

    # Set the path to Firefox executable
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    # Open browser, ie. landing page to log in
    landing_page = 'www.wikipedia.org'
    webbrowser.get('firefox').open_new(landing_page)

    # Open each URL in Firefox
    for ing in ingredients:
        try:
            url = urls[ing.name]
        except KeyError:
            print(f"Key '{ing.name}' has no url.")
            continue  # No key in dict => continue loop
        webbrowser.get('firefox').open_new_tab(url)
