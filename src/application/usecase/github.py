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

    def _get_mavis_repo(self) -> Repository.Repository:
        """Get mavis github repo"""
        return self.action_github_repo.get_repo(MAVIS_OWNER, MAVIS_REPO)

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

        mavis_pr_base_branch_name = self.analysis_target_branch_name()

        # Get or create auto pr branch
        mavis_pr_head_branch_ref = self.get_or_create_auto_pr_branch(branch_name=mavis_pr_base_branch_name)

        # fetch content and update helm file and commit changes
        self.update_helm_and_commit(ref=mavis_pr_head_branch_ref)

        # create pull request
        self.create_pull_request(head=mavis_pr_head_branch_ref.ref, base=mavis_pr_base_branch_name)

    def update_helm_and_commit(self, ref: GitRef.GitRef, file_path: str = "helmfile.yaml") -> None:
        mavis_github_repo = self._get_mavis_repo()

        content_file = self.action_github_repo.get_file(file_path, ref, github_repo=mavis_github_repo)

        if isinstance(content_file, list):
            raise MultipleFileFoundError(f"Multiple files found for {file_path} | ref={ref}")

        if content_file.content is None:
            raise NoContentError(f"{file_path} found no content")

        _raw_content = base64.b64decode(content_file.content).decode('utf-8')

        # analysis raw yaml content and update helmfile
        _clean_content = FileAdjustUseCase.replace_app_version(self.data, _raw_content)

        # Update helm file and commit changes
        # Commit file change to the commit sha we clone
        mavis_github_repo.update_file(
            path=file_path,
            message="update README.md",
            content=_clean_content,
            sha=content_file.sha,
            branch=ref.ref
        )

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

    def analysis_target_branch_name(self) -> str:
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

    def create_pull_request(
        self,
        head: str,
        base: str,
        title: str | None = None,
        body: str | None = None
    ) -> None:
        """
        Create a pull request to specify branch.
        Merge head to base.

        :param head: New Pull Request Base Branch Name. IMPORTANT: Don't need to add 'heads' prefix to branch name
        :type branch_name: str
        :param base: New Pull Request Base Branch Name. IMPORTANT: Don't need to add 'heads' prefix to Base name
        :type base: str
        :param title: New Pull Request Title
        :type title: str
        :param body: New Pull Request Body
        :type body: str
        """

        pr_title = title or "[Auto Pull Request] Update helmfile for micro service"
        f"'{self.data.target_repo}' appVersion to {self.data.target_app_version}"
        pr_body = body or f"""{pr_title}"""

        mavis_repo = self._get_mavis_repo()

        mavis_repo.create_pull(
            title=pr_title,
            body=pr_body,
            base=base,
            head=head
        )
#         """"""

#         mavis_repo = self._get_mavis_repo()
#         mavis_repo.create_pull(
#             title=f"This is a pull request for new feature {index}",
#             body="""SUMMARY
# Change HTTP library used to send requests

# TESTS
# - [x] Send 'GET' request
# - [x] Send 'POST' request with/without body""",
#             base="main",
#             head=new_branch_name
#         )
