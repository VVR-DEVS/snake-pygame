from abc import ABC, abstractmethod

class Screen(ABC):

    @abstractmethod
    def run(self, window, context):
        pass