"""Compatibility entry point for public documentation checks."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('check_public_docs.py')), run_name='__main__')
