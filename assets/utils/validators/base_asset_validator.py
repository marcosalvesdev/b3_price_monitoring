from abc import ABC, abstractmethod


class BaseAssetValidator(ABC):
    @property
    @abstractmethod
    def is_valid(self) -> bool: ...
