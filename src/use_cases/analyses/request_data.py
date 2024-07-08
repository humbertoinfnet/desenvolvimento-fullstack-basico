from dataclasses import dataclass
from src.interface_adapters.request_data.request_data_interface import RequestDataInterface


@dataclass
class RequestData:
    request_data: RequestDataInterface

    def execute_(self):
        return self.request_data.execute()
    
    def execute(self) -> dict:
        from tinydb import TinyDB, Query

        # Abrir (ou criar) um banco de dados TinyDB
        db = TinyDB('files/database/kvstore_tinydb.json')
        KeyValue = Query()
        return db.get(KeyValue.analyses_id == 1).get('data')
