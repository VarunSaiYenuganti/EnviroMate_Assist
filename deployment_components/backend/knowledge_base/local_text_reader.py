from knowledge_base.document_reader_interface import DocumentReaderInterface
from pathlib import Path

class LocalTextReader(DocumentReaderInterface):
    """Text loader for .txt from local disk"""

    def __init__(self, rooth_path:str) -> None:
        super().__init__(rooth_path)
        self.raw_text = ""
        assert Path(self.root_path).suffix == ".txt"

    def load_document(self) -> str:

        with open(self.root_path,'r', encoding="utf-8") as f:
            self.raw_text = f.read()
        return self.raw_text