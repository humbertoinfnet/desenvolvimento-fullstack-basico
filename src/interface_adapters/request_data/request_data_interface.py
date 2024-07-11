from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RequestDataInterface(ABC):
    document: str

    @abstractmethod
    def execute(self):
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def _request_data(self):
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def _adapter(self, data: dict):
        raise NotImplementedError('Método não implementado')
