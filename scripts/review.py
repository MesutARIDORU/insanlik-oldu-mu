#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İnsanlık öldü mü? · interactive review page

Compares the original text with the rewrite and builds a single-file HTML page where the user
goes through the changes one by one. The page itself comes from the shared notebook (notebook/,
copied from MesutARIDORU/notebook-review); this script gives it the skill's product file and audit.

Usage:
  python3 review.py --before old.txt --after new.txt
  python3 review.py --before old.txt --after new.txt --notes notes.json --title "Blog yazısı" --open
  python3 review.py --before before --after after --notes - --live --open <<'JSON'   # texts saved with audit.py --save
  {...}
  JSON

With --live the page is served through the local bridge (bridge.py): the page asks the agent for
other options and sends the decisions straight back to it. If the bridge cannot start, the page
stays a plain file. The notes format is described in notebook/page.py.

Uses only the Python 3 standard library.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import audit  # noqa: E402
import bridge  # noqa: E402
from notebook import page  # noqa: E402
from notebook.product import load_product  # noqa: E402

if __name__ == "__main__":
    page.main(load_product(os.path.join(HERE, "..", "notebook.json")), audit, bridge, bridge.__file__)
