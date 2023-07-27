import os

import pytest
from pydantic_core._pydantic_core import ValidationError


def test_github_env():
    if "GITHUB_ACCESS_TOKEN" in os.environ:
        from src.application.config import github_env
        assert github_env.access_token == os.environ["GITHUB_ACCESS_TOKEN"]
    else:
        with pytest.raises(ValidationError):
            from src.application.config import github_env
