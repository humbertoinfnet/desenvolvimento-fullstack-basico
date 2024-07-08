from dataclasses import dataclass

from .analyses_decision import AnalysesDecision
from .analyses_limit import AnalysesLimit
from src.interface_adapters.database.controllers.analyses import Motorinterface
from src.interface_adapters.request_data.request_data_interface import RequestDataInterface
from .request_data import RequestData


@dataclass
class Runner:
    document: str
    type_policy: str
    request_data: RequestDataInterface
    motor: Motorinterface

    def execute(self) -> dict:
        data_request = RequestData(self.request_data).execute()
        data = data_request.copy()
        response_limit = AnalysesLimit(self.document, data).execute()
        data.update(response_limit)
        response_decision = AnalysesDecision(self.document, self.type_policy, self.motor, data).execute()
        
        data_response = {
            'politica_limite': response_limit,
            'politica_regras': response_decision
        }
        self.save_analyses(data_request, data_response)
        return {
            'data_response': data_response,
            'data_request': data_request.get('data')
        }

    def save_analyses(self, data_request, data_response):
        id_insert_data = self.save_json(data_request, data_response)
        # data = self.request_data()

    def save_json(self, data_request, data_response):
        from tinydb import TinyDB, Query
        with TinyDB('files/database/kvstore_tinydb.json') as db:
            id_insert_data = db.insert({'item': 'data', 'analyses_id': 3, 'data_request': data_request, 'data_response': data_response})
        return id_insert_data