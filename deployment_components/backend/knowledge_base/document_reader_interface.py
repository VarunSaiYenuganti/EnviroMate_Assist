"""An interface for loading text from different sources"""
from abc import ABC, abstractmethod

class DocumentReaderInterface(ABC):
    """An interface for different ways to read documents"""

    def __init__(self, root_path) -> None:
        """
        Document reader interface constructor

        :param root_path: root path to where document is located
        """
        self.root_path = root_path

    @abstractmethod
    def load_document(self) -> str:
        """An abstract method for loading documents and returning them as text
        """
        pass