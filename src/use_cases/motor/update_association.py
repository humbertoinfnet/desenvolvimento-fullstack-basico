from dataclasses import dataclass
from flask import current_app
from typing import Literal
from src.interface_adapters.database.controllers.motor import Motorinterface


@dataclass
class UpdateAssociation:
    """
    Classe responsável por tratar o DELETE das associações de acordo com a alteração dos elementos principais: Policy, Layer e Rule.
    """
    motor: Motorinterface

    def update_association_rules_to_layers(self, index_id: int, type_index: Literal['association_id', 'layer_id', 'rule_id']) -> None:
        """
        Método responsável por alterar o status para inactive para as associações de regra com camada
        """

        current_app.logger.info('[UpdateAssociation] - executa metodo update_association_rules_to_layers')
        association_rules_to_layers = self.motor.get_association_rule_to_layer_by_id(type_index, [index_id])
        association_rules_to_layers['status'] = 'inactive'
        association_rules_to_layers.rename(columns={'association_id': 'id'}, inplace=True)
        if len(association_rules_to_layers):
            self.motor.update_item('rules_to_layers', association_rules_to_layers[['id', 'status']].to_dict(orient='records'))
    
    def update_association_policys_to_layers(self, index_id: int, type_index: Literal['association_id', 'layer_id', 'policy_id']) -> None:
        """
        Método responsável por alterar o status para inactive para as associações de camada com política
        """

        current_app.logger.info('[UpdateAssociation] - executa metodo update_association_policys_to_layers')
        association_policys_to_layers = self.motor.get_association_layer_to_police_by_id(type_index, [index_id])
        association_policys_to_layers['status'] = 'inactive'
        association_policys_to_layers.rename(columns={'association_id': 'id'}, inplace=True)
        if len(association_policys_to_layers):
            self.motor.update_item('layers_to_policys', association_policys_to_layers[['id', 'status']].to_dict(orient='records'))