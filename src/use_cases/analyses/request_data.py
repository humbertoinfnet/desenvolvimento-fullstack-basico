from dataclasses import dataclass
from src.interface_adapters.request_data.request_data_interface import RequestDataInterface


@dataclass
class RequestData:
    request_data: RequestDataInterface

    def execute(self):
        return self.request_data.execute()
