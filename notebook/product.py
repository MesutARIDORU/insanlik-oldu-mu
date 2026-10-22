# -*- coding: utf-8 -*-
"""Notebook review · the product a page and a bridge belong to

Every skill that uses the notebook describes itself in a product file (notebook.json at the skill
root): its name, slug and language, the pattern names its notes refer to, and any text it wants
to say differently. The notebook's own texts come from strings/<language>.json; a key in the
product's "strings" overrides the default.

  {
    "name": "Still Human?",
    "slug": "still-human",
    "language": "en",
    "title_html": "Still Human<b>?</b>",
    "date_format": "%Y-%m-%d %H:%M",
    "root_env": "STILL_HUMAN_ROOT",
    "patterns": {"R1": "Contrast polish"},
    "strings": {"bridge.event_send_next": "..."}
  }

Uses only the Python 3 standard library.
"""

import html
import json
import os
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STRINGS_DIR = os.path.join(HERE, "strings")
TEMPLATE = os.path.join(HERE, "template.html")


def load_strings(language):
    path = os.path.join(STRINGS_DIR, f"{language}.json")
    if not os.path.exists(path):
        path = os.path.join(STRINGS_DIR, "en.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class Product:
    def __init__(self, data, root=None):
        self.root = root
        self.name = data["name"]
        self.slug = data["slug"]
        self.language = data.get("language") or "en"
        self.title_html = data.get("title_html") or html.escape(self.name)
        self.date_format = data.get("date_format") or "%Y-%m-%d %H:%M"
        self.root_env = data.get("root_env")
        self.patterns = data.get("patterns") or {}
        self.strings = load_strings(self.language)
        self.strings.update(data.get("strings") or {})

    # where this product keeps its files: settings in ~/.config/<slug>, live sessions in the temp folder
    @property
    def config_dir(self):
        return os.path.join(os.path.expanduser("~"), ".config", self.slug)

    @property
    def temp_dir(self):
        return (self.root_env and os.environ.get(self.root_env)) or os.path.join(tempfile.gettempdir(), self.slug)

    def t(self, key, **values):
        """The text for key in the product's language, with {placeholders} filled in."""
        text = self.strings.get(key, key)
        if isinstance(text, dict):
            text = text.get("one" if values.get("n") == 1 else "other", "")
        values = dict(values, product=self.name, slug=self.slug)
        return text.format(**values) if isinstance(text, str) else text

    def page_strings(self):
        """The texts the page uses in the browser, with the product's name and slug already filled in."""
        out = {}
        for key, value in self.strings.items():
            if key.startswith(("bridge.", "cli.")):
                continue  # used in Python only
            if isinstance(value, str) and ("{product}" in value or "{slug}" in value):
                value = value.replace("{product}", self.name).replace("{slug}", self.slug)
            out[key] = value
        return out


def load_product(path):
    with open(path, encoding="utf-8") as f:
        return Product(json.load(f), root=os.path.dirname(os.path.abspath(path)))
