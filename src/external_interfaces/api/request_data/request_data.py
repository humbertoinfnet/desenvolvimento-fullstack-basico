import requests
from dataclasses import dataclass
from src.interface_adapters.request_data.request_data_interface import RequestDataInterface


@dataclass
class RequestData(RequestDataInterface):
    document: str

    def __post_init__(self):
        self.params = {}
        self.response = {}
        self.data = {}

    def execute(self):
        self.params_to_request_api()
        self._request_data()
        self._adapter()
        return self.data

    def params_to_request_api(self):
        self.params = {
            'url': 'http://localhost:3000/customer-information',
            'params': self.document
        }

    def _request_data(self):
        self.response = requests.get(**self.params).json()

    def _adapter(self):
        self.data = self.response.copy()
        del self.response
