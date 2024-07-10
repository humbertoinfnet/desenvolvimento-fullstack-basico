from dataclasses import dataclass
from tinydb import TinyDB
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

    def save_analyses(self, data_request: dict, data_response: dict):
        id_analyses_detail = self.save_json(data_request, data_response)
        data_save = self.handle_data_save(id_analyses_detail, data_response)
        self.motor.add_item_analyses(data_save)

    def save_json(self, data_request: dict, data_response: dict):
        with TinyDB('files/database/analyses_detail.json') as db:
            id_analyses_detail = db.insert({'item': 'data', 'analyses_id': 3, 'data_request': data_request, 'data_response': data_response})
        return id_analyses_detail
    
    def handle_data_save(self, id_analyses_detail: int, data_response: dict) -> list[dict]:
        return [
            {
                'document': self.document,
                'type_policy': self.type_policy,
                'limit': data_response.get('politica_limite', {}).get('limit_calc', 0),
                'decision': data_response.get('politica_regras', {}).get('decision'),
                'analyses_detail_id': id_analyses_detail,
            }
        ]