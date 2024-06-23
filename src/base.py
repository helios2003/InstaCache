from abc import ABC, abstractmethod

class Cache(ABC):
    """
    An abstract class for cache from which all the other caches inherit.
    """
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

    @abstractmethod
    def set(self, key: int, value: str) -> str:
        pass

    @abstractmethod
    def get(self, key: int) -> str:
        pass

    @abstractmethod
    def delete(self, key: int) -> str:
        pass

    @abstractmethod
    def view() -> None:
        pass
