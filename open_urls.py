import webbrowser
import sys


def open_ingredient_urls(ingredients: list[str], urls: dict[str, str]):
    firefox_path = "/usr/bin/firefox"
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    # Open browser, ie. landing page to log in
    landing_page = 'www.wikipedia.org'
    webbrowser.get('firefox').open_new(landing_page)

    # Open each URL in Firefox
    for ing in ingredients:
        try:
            url = urls[ing]
        except KeyError:
            print(f"Key '{ing}' has no url.", file=sys.stderr)
            continue  # No key in dict => continue loop
        webbrowser.get('firefox').open_new_tab(url)
