"""Vercel serverless entry-point. Exposes the FastAPI ASGI app."""
from __future__ import annotations

import sys
import os

# Ensure the src/ directory is on the Python path so `aiseo.*` imports resolve
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.insert(0, _src)

from aiseo.api.app import create_app  # noqa: E402

app = create_app()
