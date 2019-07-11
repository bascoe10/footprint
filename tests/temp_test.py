import os, sys
print(os.path.abspath(os.path.dirname(__file__)))
from .context import footprint
from footprint.cli import FootPrint

import pytest, inspect

def test_footprint_import():
    assert inspect.isclass(FootPrint), 'FootPrint class is available in cli'

def test_footprint_with_bare_repo():
    with pytest.raises(AttributeError):
        FootPrint('./tests/test_repo.git', [], './test_repo.git')