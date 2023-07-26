

from dataclasses import FrozenInstanceError
from src.domain.model.action import UpdateHelmByMicroSvcModel
import pytest


def test_frozen_dataclass_cannot_change():
    model = UpdateHelmByMicroSvcModel(base="", head="", target_repo="", target_app_version="")

    with pytest.raises(FrozenInstanceError):
        model.base = "changed"

    with pytest.raises(FrozenInstanceError):
        model.head = "changed"

    with pytest.raises(FrozenInstanceError):
        model.target_repo = "changed"

    with pytest.raises(FrozenInstanceError):
        model.target_app_version = "changed"
