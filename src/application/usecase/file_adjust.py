import re

from common.constants import FIND_SPECIFY_MICROSVC_RE
from domain.model.action import UpdateHelmByMicroSvcModel


class FileAdjustUseCase:
    @staticmethod
    def replace_app_version(data: UpdateHelmByMicroSvcModel, raw_content: str) -> str:
        """replace app version in file

        Args:
            data (UpdateHelmByMicroSvcModel): update helm by micro svc model
            raw_content (str): raw file content

        Returns:
            str: clean file content

        Notes:
            - use re.DOTALL to replace all line
            - use re.sub to replace all app version in file
            - use lambda to replace app version in file
            - use groupdict to get app version group
            - use group to get app version group
            - use group.groupdict() to get app version group dict
            - use group.group() to get app version group string

        """

        def group_adjust_fn(m: re.Match) -> str:
            return str(m.group().replace(m.groupdict()["appVersion"], data.target_app_version))

        pattern = FIND_SPECIFY_MICROSVC_RE.format(data.target_repo)
        return re.sub(pattern, group_adjust_fn, raw_content, flags=re.DOTALL)
