# plugins/plugin_base.py
from abc import ABC, abstractmethod

class Plugin(ABC):
    """
    Abstract base class for all plugins. All plugins must implement these methods.
    """
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def teardown(self):
        pass
