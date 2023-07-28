import os

import pytest
from pydantic_core._pydantic_core import ValidationError


def test_github_env_exists():
    if not "GITHUB_ACCESS_TOKEN" in os.environ:
        os.environ["GITHUB_ACCESS_TOKEN"] = "test"

    from src.application.config import github_env
    assert github_env.access_token == os.environ["GITHUB_ACCESS_TOKEN"]

def test_github_env_not_exists():
    if "GITHUB_ACCESS_TOKEN" in os.environ:
        del os.environ["GITHUB_ACCESS_TOKEN"]

    with pytest.raises(ValidationError):
        from src.application.config import github_env
        assert github_env.access_token == os.environ["GITHUB_ACCESS_TOKEN"]
