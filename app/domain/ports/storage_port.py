from abc import ABC, abstractmethod
from typing import BinaryIO

class StoragePort(ABC):
    @abstractmethod
    def upload_file(self, file_stream: BinaryIO, filename: str, content_type: str) -> str:
        pass