from github import Auth, ContentFile, Github, GitRef, Repository

from common.constants import MAVIS_MAIN_BRANCH
from domain.model.env import GithubEnv

from repository.github_repo import GithubRepositoryBase


class GithubRepository(GithubRepositoryBase):
    """"""

    def __init__(self, secret: GithubEnv) -> None:
        self._auth_obj = Auth.Token(secret.access_token)
        self._github_obj = Github(auth=self._auth_obj)

    def get_repo(self, owner: str, repo_name: str) -> Repository.Repository:
        return self._github_obj.get_repo(f"{owner}/{repo_name}")

    def get_branch_from_repo(self, github_repo: Repository.Repository, branch_name: str) -> GitRef.GitRef:
        return github_repo.get_git_ref(ref=f"heads/{branch_name}")

    def get_file(
        self,
        file_path: str,
        ref: GitRef.GitRef,
        github_repo: Repository.Repository,
    ) -> ContentFile.ContentFile | list[ContentFile.ContentFile]:
        return github_repo.get_contents(path=file_path, ref=ref.ref)

    def create_branch(
        self,
        github_repo: Repository.Repository,
        branch_name: str,
        branching_from: str = MAVIS_MAIN_BRANCH,
    ) -> GitRef.GitRef:
        return github_repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=github_repo.get_branch(branching_from).commit.sha
        )
