import pytest

from src.application.usecase.file_adjust import FileAdjustUseCase
from src.domain.model.action import UpdateHelmByMicroSvcModel

RAW_HELM_FIEL_CONTENTS = [
    """
- name: example-app
  <<: *anchor
  needs:
  - example-main-app
  chart: example/pare-example
  version: 0.5.0
  values:
    - image: preview.example.com/example-app
    - appVersion: 01-abcdef6
    """,
    """
- name: example-app
  values:
    - appVersion: 01-abcdef6
    """,
    """
- name: example-app
  <<: *anchor
  needs:
  - example-main-app
  chart: example/pare-example
  version: 0.5.0
  values:
    - image: preview.example.com/example-app
    - appVersion: 01-abcdef6
    """,
    """
- name: example-app
  values:
    - image: preview.example.com/example-app
    - appVersion: 01-abcdef6
    - extraContainer:
        image: preview.example.com/example-app
        appVersion: 0.0.0
        pullPolicy: Always
        """,
    """
- name: example-app
  values:
    - image: preview.example.com/example-app
    - appVersion: not_a_target
    - extraContainer:
        image: preview.example.com/example-app
        appVersion: 0.0.0
        pullPolicy: Always
- name: example-app-2
  values:
    - image: preview.example.com/example-app
    - appVersion: 01-abcdef6
    - extraContainer:
        image: preview.example.com/example-app
        appVersion: 0.0.0
        pullPolicy: Always
- name: example-app-3
  values:
    - image: preview.example.com/example-app
    - appVersion: not_a_target
    - extraContainer:
        image: preview.example.com/example-app
        appVersion: 0.0.0
        pullPolicy: Always""",
]

SPACE_PREFIX_RAW_HELM_FIEL_CONTENTS = [
    """
    - name: example-app
    values:
        - image: preview.example.com/example-app
        - appVersion: not_a_target
        - extraContainer:
            image: preview.example.com/example-app
            appVersion: 0.0.0
            pullPolicy: Always
    """,
    """
    - name: example-app
        values:
            - image: preview.example.com/example-app
            - appVersions: not_a_target
        - extraContainer:
            image: preview.example.com/example-app
            appVersion: 0.0.0
            pullPolicy: Always
    """,
]


@pytest.mark.parametrize(
    "data,raw_content",
    [
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            RAW_HELM_FIEL_CONTENTS[0],
        ),
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            RAW_HELM_FIEL_CONTENTS[1],
        ),
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            RAW_HELM_FIEL_CONTENTS[2],
        ),
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            RAW_HELM_FIEL_CONTENTS[3],
        ),
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app-2", target_app_version="20-example"),
            RAW_HELM_FIEL_CONTENTS[4],
        ),
    ],
)
def test_replace_appversion_with_different__appversion_position(
    data: UpdateHelmByMicroSvcModel, raw_content: str
):
    correct_answer = raw_content.replace("01-abcdef6", data.target_app_version, 1)
    assert FileAdjustUseCase.replace_app_version(data=data, raw_content=raw_content) == correct_answer


@pytest.mark.parametrize(
    "data,raw_content",
    [
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            SPACE_PREFIX_RAW_HELM_FIEL_CONTENTS[0],
        ),
        (
            UpdateHelmByMicroSvcModel(base="", head="", target_repo="example-app", target_app_version="20-example"),
            SPACE_PREFIX_RAW_HELM_FIEL_CONTENTS[1],
        ),
    ],
)
def test_replace_appversion_with_space_prefix_name(data: UpdateHelmByMicroSvcModel, raw_content: str):
    assert FileAdjustUseCase.replace_app_version(data=data, raw_content=raw_content) == raw_content
