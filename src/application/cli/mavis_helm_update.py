from typer import Typer

from application.config import github_env
from application.usecase.github import GithubManager
from common.constants import MAVIS_REPO
from domain.model.action import UpdateHelmByMicroSvcModel
from infra.github import GithubRepository

action_app = Typer()


@action_app.command()
def pull_request(base: str, head: str, target_repo: str, target_repo_app_version: str, pr_to: str = MAVIS_REPO) -> None:
    """Send pull request to mavis"""
    # Gather data
    action_data = UpdateHelmByMicroSvcModel(base, head, target_repo, target_repo_app_version, pr_to)

    action_github_repo = GithubRepository(github_env)

    # Use Case
    manager = GithubManager(action_github_repo, action_data)
    manager.update_helm_and_pr()
