import os, sys
print(os.path.abspath(os.path.dirname(__file__)))
from .context import footprint
from footprint.cli import FootPrint
from footprint.exceptions import RepoNotFoundException, BareRepoException

import pytest, inspect

def test_footprint_import():
    assert inspect.isclass(FootPrint), 'FootPrint class is available in cli'

def test_footprint_non_git_repo():
    with pytest.raises(RepoNotFoundException):
        FootPrint('./tests/non_git_repo', [], './non_git_repo')

def test_footprint_with_bare_repo():
    with pytest.raises(BareRepoException):
        FootPrint('./tests/test_repo_bare.git', [], './test_repo_bare.git')