import os, sys
print(os.path.abspath(os.path.dirname(__file__)))
from .context import footprint
import footprint.cli

import pytest, inspect

def test_footprint_import():
    assert inspect.isclass(footprint.cli.FootPrint), 'FootPrint class is available in cli'

