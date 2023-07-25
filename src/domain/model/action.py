from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class UpdateHelmByMicroSvcModel:
    """
    Contain all data fro github action

    :param base: Branch merge into
    :type base: str
    :param head: Branch merge from
    :type head: str
    :param target: microservice name
    :type target: str
    :param target_app_version: microservice app version
    :type target_app_version: str

    :param mavis_owner: mavis owner
    :type target_app_version: str
    :param mavis_reponame: mavis repo name
    :type target_app_version: str
    """

    __slots__ = (
        "base",
        "head",
        "target_repo",
        "target_app_version",
        "mavis_owner",
        "mavis_reponame",
    )

    base: str
    head: str
    target_repo: str
    target_app_version: str

    mavis_owner: Final[str] = "pnetwork"
    mavis_reponame: Final[str] = "mavis"
