import os

import pytest
from pydantic_core._pydantic_core import ValidationError

from src.domain.model.env import GithubEnv


def test_githubenv_init_from_environment():
    os.environ["GITHUB_ACCESS_TOKEN"] = "test"

    env = GithubEnv()
    assert env.access_token == "test"

    os.unsetenv("GITHUB_ACCESS_TOKEN")


def test_githubenv_init_without_environment():
    if "GITHUB_ACCESS_TOKEN" in os.environ:
        del os.environ["GITHUB_ACCESS_TOKEN"]

    with pytest.raises(ValidationError):
        env = GithubEnv()
        assert env.access_token == "test"
