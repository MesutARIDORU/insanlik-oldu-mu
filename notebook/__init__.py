# -*- coding: utf-8 -*-
"""Notebook review: the review page and the live bridge shared by the humanizer skills.

The folder is copied into every skill as notebook/ (see tools/sync.py); a skill describes itself
in notebook.json and calls page.main() and bridge.main() from its own scripts.
"""

import os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION"), encoding="utf-8") as _f:
    __version__ = _f.read().strip()
