import os

from src.domain.model.env import GithubEnv
from src.infra.github import GithubRepository


def test_infra_githubrepository_init():
    # TODO: Not done yet
    os.environ["GITHUB_ACCESS_TOKEN"] = "test"

    repository = GithubRepository(GithubEnv())
    # assert repository is not None
