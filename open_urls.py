import subprocess


def open_ingredient_urls(ingredient_names: list[str], icu_dict: dict[str, str]) -> list[str]:
    """
    Open ingredients, ie. their urls in firefox with the supermarket profile (in my case with "Rewe")
    Return list of `Ingredient`s without an URL.
    """
    # TODO: Profilpfad in Config-Datei auslagern <16-01-2024>
    firefox = "firefox --profile /home/philipp/.mozilla/firefox/5mud7ety.Rewe"

    ing_missing_url: list[str] = []

    # Open each URL
    urls = []
    for ing_name in ingredient_names:
        try:
            urls.append(icu_dict[ing_name][1])
        except KeyError:
            print(f'Ingredient "{ing_name}" has no url.')
            ing_missing_url.append(ing_name)
    # subpress warnings from firefox
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)

    return ing_missing_url
