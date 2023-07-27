import base64
import logging

from github import GitRef, Repository, UnknownObjectException

from src.application.usecase.exceptions import MultipleFileFoundError, NoContentError
from src.common.constants import MAVIS_MAIN_BRANCH, MAVIS_OWNER, MAVIS_REPO
from src.domain.model.action import UpdateHelmByMicroSvcModel
from src.infra.github import GithubRepository

logger = logging.getLogger(__name__)


class GithubManager():

    def __init__(self, repo: GithubRepository, action_data: UpdateHelmByMicroSvcModel) -> None:
        """
        :param repo: Repository object of Github Action.
        :type repo: GithubRepository
        :param action_data: Update.
        :type action_data: UpdateHelmByMicroSvcModel
        """
        self.action_github_repo = repo
        self.data = action_data

    def update_helm_and_pr(self) -> None:

        mavis_pr_base_branch_name = self.analyze_target_branch_name()

        ref = self.get_or_create_auto_pr_branch(branch_name=mavis_pr_base_branch_name)

        self.update_helm(ref=ref)


    def update_helm(self, ref: GitRef.GitRef, file_path: str = "helmfile.yaml") -> None:
        content_file = self.action_github_repo.get_file(file_path, ref, github_repo=self._get_mavis_repo())

        if isinstance(content_file, list):
            raise MultipleFileFoundError(f"Multiple files found for {file_path} | ref={ref}")

        if content_file.content is None:
            raise NoContentError(f"{file_path} found no content")

        _raw_content = base64.b64decode(content_file.content).decode('utf-8')

        # TODO : analysis raw yaml content and update helmfile

        # TODO: Update helm file and commit changes
        # self.commit_changes()

    def get_or_create_auto_pr_branch(self, branch_name: str) -> GitRef.GitRef:
        """Create a new branch to mavis repo if not exists
        If exists, then reture that branch

        :return: New Pull Request Base Branch Name
        :rtype: GitRef.GitRef
        """
        mavis_github_repo = self._get_mavis_repo()
        try:
            return self.action_github_repo.create_git_ref(mavis_github_repo, branch_name=branch_name)
        except Exception as e:
            logger.warning(e)
            return self.action_github_repo.get_git_ref(mavis_github_repo, branch_name)

    def _get_mavis_repo(self) -> Repository.Repository:
        """Get mavis github repo"""
        return self.action_github_repo.get_repo(MAVIS_OWNER, MAVIS_REPO)

    def analyze_target_branch_name(self) -> str:
        """
        The base branch of a pull request can be either "master" or
        the same as the head branch name that triggered the GitHub Action pull request event.

        :return: New Pull Request Base Branch Name
        :rtype: str
        """
        try:
            return self.action_github_repo.get_branches_from_repo(
                self._get_mavis_repo(),
                self.data.head
            ).ref.lstrip("refs/heads/")
        except UnknownObjectException:
            return MAVIS_MAIN_BRANCH
