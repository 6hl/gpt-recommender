from abc import ABC, abstractmethod


class DefaultParser(ABC):

    @abstractmethod
    def parse(self):
        raise NotImplementedError
