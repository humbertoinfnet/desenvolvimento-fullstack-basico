from abc import abstractmethod
import pandas as pd
from typing import Literal
from src.external_interfaces.database.controllers.templates import MotorTemplate


class Motorinterface(MotorTemplate):
    
    @abstractmethod
    def get_all_policys(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_policys_by_id(self, policys_id: list) -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_all_layers(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_layers_by_id(self, layers_id: list) -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_all_rules(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_rules_by_id(self, rules_id: list) -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def get_all_association_rule_to_layer(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')
  
    @abstractmethod
    def get_association_rule_to_layer_by_id(self, type_id: Literal['association_id', 'layer_id', 'rule_id'], index_ix: list[int]) -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')
  
    @abstractmethod
    def get_all_association_layer_to_police(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def get_association_layer_to_police_by_id(self, type_id: Literal['association_id', 'policy_id', 'layer_id'], index_ix: list[int]) -> pd.DataFrame:
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def add_item(self, name_table: str, data_save: list[dict]):
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def update_item(self, name_table: str, data_update: list[dict]):
        raise NotImplementedError('Método não implementado')
