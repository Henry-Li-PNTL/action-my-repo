from typer import Typer

from src.application.usecase.github import GithubManager
from src.domain.model.action import UpdateHelmByMicroSvcModel
from src.domain.model.env import GithubEnv
from src.infra.github import GithubRepository

action_app = Typer()


@action_app.command()
def pull_request(base: str, head: str, target_repo: str, target_repo_app_version: str) -> None:
    """Send pull request to mavis"""
    # Gather data
    secret = GithubEnv() # type: ignore
    action_data = UpdateHelmByMicroSvcModel(base, head, target_repo, target_repo_app_version)

    action_github_repo = GithubRepository(secret)

    # Use Case
    manager = GithubManager(action_github_repo, action_data)
    manager.update_helm_and_pr()
