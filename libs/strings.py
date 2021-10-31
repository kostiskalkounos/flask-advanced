"""
libs.strings

By default, users `en-us.json` file inside the `strings` top-level folder.

If the language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`.
"""

import json

default_locale = "en-us.json"
cached_strings = {}

def refresh() -> None:
    print("Refreshing...")
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)

def gettext(name: str) -> str:
    return cached_strings[name]

def set_default_locale(locale: str) -> None:
    global default_locale
    default_locale = locale


refresh()
