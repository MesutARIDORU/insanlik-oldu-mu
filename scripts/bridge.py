#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İnsanlık öldü mü? · live bridge

Runs the local bridge between the review page and the agent (Claude Code, Codex or Gemini CLI).
The bridge itself comes from the shared notebook (notebook/bridge.py); this script binds it to
the skill's product file.

Commands (run by the agent):
  python3 bridge.py start --page review.html [--agent claude|codex|gemini] [--open]
  python3 bridge.py wait [--timeout 540]
  python3 bridge.py reply --request N --suggestion "..." [--suggestion "..."]
  python3 bridge.py status
  python3 bridge.py close

Uses only the Python 3 standard library.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from notebook import bridge  # noqa: E402
from notebook.product import load_product  # noqa: E402

bridge.configure(load_product(os.path.join(HERE, "..", "notebook.json")), __file__)
start, call, read_info = bridge.start, bridge.call, bridge.read_info

if __name__ == "__main__":
    bridge.main()
