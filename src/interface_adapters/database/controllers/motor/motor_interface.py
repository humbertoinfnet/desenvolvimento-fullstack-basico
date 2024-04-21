from abc import abstractmethod
import pandas as pd
from typing import Literal
from src.external_interfaces.database.controllers.templates import MotorTemplate

NamesTable = Literal['policys', 'layers', 'rules', 'rules_to_layers', 'layers_to_policys']


class Motorinterface(MotorTemplate):
    
    @abstractmethod
    def get_all_policys(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        """
        Método responsável por buscar todas as políticas registradas em banco com o filtro de status.

        Returns:
            Dataframe com as colunas: [
                "policy_id",
                "name",
                "description",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_policys_by_id(self, policys_id: list) -> pd.DataFrame:
        """
        Método responsável por buscar políticas por id.

        Returns:
            Dataframe com as colunas: [
                "policy_id",
                "name",
                "description",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_all_layers(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        """
        Método responsável por buscar todas as camadas registradas em banco com o filtro de status.

        Returns:
            Dataframe com as colunas: [
                "layer_id",
                "name",
                "description",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_layers_by_id(self, layers_id: list) -> pd.DataFrame:
        """
        Método responsável por buscar camadas por id.

        Returns:
            Dataframe com as colunas: [
                "layer_id",
                "name",
                "description",
                "identify",
            ]
        
        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_all_rules(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        """
        Método responsável por buscar todas as regras registradas em banco com o filtro de status.

        Returns:
            Dataframe com as colunas: [
                "rule_id",
                "name",
                "code",
                "description",
                "identify",
                "rule",
            ]
        
        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def get_rules_by_id(self, rules_id: list) -> pd.DataFrame:
        """
        Método responsável por buscar regras por id.

        Returns:
            Dataframe com as colunas: [
                "rule_id",
                "name",
                "code",
                "description",
                "identify",
                "rule",
            ]
        
        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def get_all_association_rule_to_layer(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        """
        Método responsável por buscar todas as associações de regra com camada registradas em banco com o filtro de status.

        Returns:
            Dataframe com as colunas: [
                "association_id",
                "name_layer",
                "name_rule",
                "layer_id",
                "rule_id",
                "action",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
  
    @abstractmethod
    def get_association_rule_to_layer_by_id(self, type_id: Literal['association_id', 'layer_id', 'rule_id'], index_ix: list[int]) -> pd.DataFrame:
        """
        Método responsável por buscar associações de regra com camada por id.

        Returns:
            Dataframe com as colunas: [
                "association_id",
                "name_layer",
                "name_rule",
                "layer_id",
                "rule_id",
                "action",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
  
    @abstractmethod
    def get_all_association_layer_to_police(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        """
        Método responsável por buscar todas as associações de camada com política registradas em banco com o filtro de status.

        Returns:
            Dataframe com as colunas: [
                "association_id",
                "name_layer",
                "name_policy",
                "policy_id",
                "layer_id",
                "priority",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def get_association_layer_to_police_by_id(self, type_id: Literal['association_id', 'policy_id', 'layer_id'], index_ix: list[int]) -> pd.DataFrame:
        """
        Método responsável por buscar associações de camada com política por id.

        Returns:
            Dataframe com as colunas: [
                "association_id",
                "name_layer",
                "name_policy",
                "policy_id",
                "layer_id",
                "priority",
                "identify",
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def add_item(self, name_table: NamesTable, data_save: list[dict]):
        """
        Método responsável por salvar novos registros em banco.

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')

    @abstractmethod
    def update_item(self, name_table: NamesTable, data_update: list[dict]):
        """
        Método responsável por atualizar registros em banco

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
