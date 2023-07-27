from abc import abstractmethod
from typing import Any

from github import ContentFile, GitRef, Repository

from src.common.constants import MAVIS_MAIN_BRANCH

from . import GenericRepository


class GithubRepositoryBase(GenericRepository):

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_repo(self, owner: str, repo_name: str) -> Repository.Repository:
        raise NotImplementedError

    @abstractmethod
    def get_branch_from_repo(self, github_repo: Repository.Repository, branch_name: str) -> GitRef.GitRef:
        raise NotImplementedError

    @abstractmethod
    def get_file(
        self,
        file_path: str,
        ref: GitRef.GitRef,
        github_repo: Repository.Repository,
    ) -> ContentFile.ContentFile | list[ContentFile.ContentFile]:
        raise NotImplementedError

    @abstractmethod
    def update_file(
        self,
        file_path: str,
        commit_message: str,
        update_content: str,
        content_file: ContentFile.ContentFile,
        github_repo: Repository.Repository,
        branch_name: str
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create_branch(
        self,
        github_repo: Repository.Repository,
        branch_name: str,
        branching_from: str = MAVIS_MAIN_BRANCH,
    ) -> GitRef.GitRef:
        raise NotImplementedError
