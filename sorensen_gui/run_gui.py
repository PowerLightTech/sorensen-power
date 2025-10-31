#!/usr/bin/env python3
"""
Convenience script to run the Sorensen GUI application.

Usage:
    python run_gui.py
    OR
    python -m sorensen_gui.run_gui

Note: This script adds the parent directory to sys.path to allow importing
from the repository root. In a production environment, the package should
be properly installed using pip or setuptools.
"""

import sys
from pathlib import Path

# Add parent directory to path only if not already present
_parent_dir = str(Path(__file__).parent.parent)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from sorensen_gui.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
