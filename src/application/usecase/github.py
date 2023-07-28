import base64
import logging

from github import GitRef, Repository, UnknownObjectException

from src.application.usecase.exceptions import MultipleFileFoundError, NoContentError
from src.application.usecase.file_adjust import FileAdjustUseCase
from src.common.constants import MAVIS_MAIN_BRANCH, MAVIS_OWNER, MAVIS_REPO
from src.domain.model.action import UpdateHelmByMicroSvcModel
from src.infra.github import GithubRepository

logger = logging.getLogger(__name__)


class GithubManager():

    def _get_github_repo(self, owner: str, repo_name: str) -> Repository.Repository:
        """Get github repository

        Args:
            owner (str): Owner of Github repository
            repo_name (str): Name of Github repository

        Returns:
            Repository.Repository: Github repo
        """
        return self.action_github_repo.get_repo(owner, repo_name)

    def __init__(self, repo: GithubRepository, action_data: UpdateHelmByMicroSvcModel) -> None:
        """Init function

        Args:
            repo (GithubRepository): Repository object of Github Action
            action_data (UpdateHelmByMicroSvcModel): Update action DTO
        """
        self.action_github_repo = repo
        self.data = action_data
        self._mavis_repo = self._get_github_repo(MAVIS_OWNER, MAVIS_REPO)

    def update_helm_and_pr(self) -> None:

        mavis_pr_base_branch_name = self.get_pr_base_branch_name(self._mavis_repo, self.data.head)
        mavis_pr_head_branch_ref = self.get_or_create_auto_pr_branch(
            self._mavis_repo,
            branch_name=mavis_pr_base_branch_name
        )

        self.update_helm_and_commit(repo=self._mavis_repo, ref=mavis_pr_head_branch_ref)

        self.create_pull_request(
            repo=self._mavis_repo,
            head=mavis_pr_head_branch_ref.ref,
            base=mavis_pr_base_branch_name
        )

    def update_helm_and_commit(
        self,
        repo: Repository.Repository,
        ref: GitRef.GitRef,
        file_path: str = "helmfile.yaml"
    ) -> None:
        """Fetch Helmfile, Update appVersion,

        Args:
            repo (Repository.Repository): Github repo
            ref (GitRef.GitRef): Branch we fetch file from
            file_path (str, optional): file path. Defaults to "helmfile.yaml".

        Raises:
            MultipleFileFoundError: if multiple file found
            NoContentError: if file is not found
        """

        content_file = self.action_github_repo.get_file(file_path, ref, github_repo=repo)

        if isinstance(content_file, list):
            raise MultipleFileFoundError(f"Multiple files found for {file_path} | ref={ref}")

        if content_file.content is None:
            raise NoContentError(f"{file_path} found no content")

        _raw_content = base64.b64decode(content_file.content).decode('utf-8')

        # analysis raw yaml content and update helmfile
        _clean_content = FileAdjustUseCase.replace_app_version(self.data, _raw_content)

        # Update helm file and commit changes
        # Commit file change to the commit sha we clone
        repo.update_file(
            path=file_path,
            message=f"chore: update helmfile {self.data.target_repo} appVersion to {self.data.target_app_version}",
            content=_clean_content,
            sha=content_file.sha,
            branch=ref.ref
        )

    def get_or_create_auto_pr_branch(self, repo: Repository.Repository, branch_name: str) -> GitRef.GitRef:
        """Return the branch ref if exists
        otherwise, Create a new branch to mavis repo

        Args:
            repo (Repository.Repository): target github repo
            branch_name (str): Target branch name

        Returns:
            GitRef.GitRef: New Pull Request Base Branch Name
        """
        try:
            return self.action_github_repo.get_branch_from_repo(repo, branch_name=branch_name)
        except Exception as e:
            logger.warning(e)
            return self.action_github_repo.create_branch(repo, branch_name=branch_name)

    def get_pr_base_branch_name(
        self,
        repo: Repository.Repository,
        try_branch: str,
        default_branch: str = MAVIS_MAIN_BRANCH
    ) -> str:
        """The base branch of a pull request can be either "master" or
        the same as the head branch name that triggered the GitHub Action pull request event.

        Args:
            repo (Repository.Repository): _description_
            try_branch (str): return try_branch if exists.
            default_branch (str, optional): if try_branch is not exists, then use this default_branch name.
                                            Defaults to MAVIS_MAIN_BRANCH.

        Returns:
            str: New Pull Request Base Branch Name
        """
        try:
            return self.action_github_repo.get_branch_from_repo(
                repo,
                try_branch
            ).ref.lstrip("refs/heads/")
        except UnknownObjectException:
            return default_branch

    def create_pull_request(
        self,
        repo: Repository.Repository,
        head: str,
        base: str,
        title: str | None = None,
        body: str | None = None
    ) -> None:
        """
        Create a pull request to specify branch.
        Merge head to base.

        Args:
            repo (Repository.Repository): _description_
            head (str): New Pull Request Base Branch Name. IMPORTANT: Don't need to add 'heads' prefix to branch name
            base (str): New Pull Request Base Branch Name. IMPORTANT: Don't need to add 'heads' prefix to Base name
            title (str | None, optional): New Pull Request Title. Defaults to None.
                                          If it's None, will give a proper default title.
            body (str | None, optional): New Pull Request Body. Defaults to None.
                                         If it's None, will give a proper default body.
        """

        pr_title = title or "[Auto Pull Request] Update helmfile for micro service"
        f"'{self.data.target_repo}' appVersion to {self.data.target_app_version}"
        pr_body = body or f"""{pr_title}"""

        repo.create_pull(
            title=pr_title,
            body=pr_body,
            base=base,
            head=head
        )
