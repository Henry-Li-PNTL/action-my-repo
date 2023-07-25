from abc import ABC, abstractmethod


class GenericRepository(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()
