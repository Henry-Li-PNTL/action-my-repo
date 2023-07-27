from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateHelmByMicroSvcModel:
    """Contain all data fro github action

    Args:
        base (str): Branch merge into
        head (str): Branch merge from
        target (str): microservice name
        target_app_version (str): microservice app version
    """

    __slots__ = (
        "base",
        "head",
        "target_repo",
        "target_app_version",
    )

    base: str
    head: str
    target_repo: str
    target_app_version: str
