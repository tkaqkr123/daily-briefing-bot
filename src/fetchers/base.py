from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class FetchResult:
    label: str
    content: str
    success: bool
    error: str = field(default="")


class BaseFetcher(ABC):
    @abstractmethod
    def fetch(self) -> FetchResult:
        pass
