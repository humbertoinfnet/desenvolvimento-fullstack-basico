from abc import abstractmethod
import pandas as pd
from src.external_interfaces.database.controllers.templates import MotorTemplate


class Motorinterface(MotorTemplate):
    
    @abstractmethod
    def get_policy_rule(self, policy_name: str) -> pd.DataFrame:
        """
        Método responsável por buscar a política associada ao nome.

        Returns:
            Dataframe com as colunas: [
                policy_id
                name policy_name
                layer_id
                layer_name
                rule_id
                action
                name rule_name
                code
                rule
                description
            ]

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
    
    @abstractmethod
    def add_item_analyses(self, data_save: list[dict]) -> list:
        """
        Método responsável por salvar os dados na tabela Analyses.

        Returns:
            ids salvos

        Raises:
            NotImplementedError: função deve ser implementada nas classes que herdam da classe Motorinterface
        """
        raise NotImplementedError('Método não implementado')
