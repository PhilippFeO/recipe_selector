import subprocess


def open_ingredient_urls(ingredient_names: list[str], icu_dict: dict[str, str]) -> list[str]:
    """
    Open ingredients, ie. their urls in firefox with the supermarket profile (in my case with "Rewe")
    Return list of `Ingredient`s without an URL.
    """
    # TODO: Profilpfad in Config-Datei auslagern <16-01-2024>
    firefox = "firefox --profile /home/philipp/.mozilla/firefox/5mud7ety.Rewe"

    # TODO: Prüfen, ob diese notwendig ist <16-01-2024>
    #   Ich glaube, man kann Produkte „anonym“ in Warenkorb leben, weil man beim Bezahlen automatisch zur Anmeldung geleitet wird.
    #   Aktueller Stand: Erst anmelden und dann jede Seite aktualisieren bevor man Produkt in Warenkorb legt
    landing_page = 'https://account.rewe.de/realms/sso/protocol/openid-connect/auth?response_type=code&client_id=ecom&redirect_uri=https%3A%2F%2Fwww.rewe.de%2Fsso%2Flogin&state=4f44fbdb-c2bd-45d1-a142-771f02433d39&login=true&scope=openid'

    ing_missing_url: list[str] = []

    # Open each URL
    urls = [landing_page]
    for ing_name in ingredient_names:
        try:
            urls.append(icu_dict[ing_name][1])
        except KeyError:
            print(f'Ingredient "{ing_name}" has no url.')
            ing_missing_url.append(ing_name)
    # subpress warnings from firefox
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)

    return ing_missing_url
