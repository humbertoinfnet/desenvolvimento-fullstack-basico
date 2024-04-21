from dataclasses import dataclass
import pandas as pd
from flask import current_app
from typing import Literal, Union
from src.interface_adapters.database.controllers.motor import Motorinterface
from src.interface_adapters.schemas.motor.association import (
    BodyAssociationLayersPolicys,
    PathAssociation,
    PathLayersPolicys,
    PathRulesLayers,
    BodyPrioritys,
    BodyAssociationRulesLayers,
    QueryUpdateAssociationRulesLayers
)


@dataclass
class Association:
    """
    Método responsável pela lógica envolvendo o elemento de associações.
    """
    motor: Motorinterface


    def get_all_association(self, type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para buscar todos as associações.
        """

        current_app.logger.info('[Association] - executa metodo get_all_association')
        if type_association == 'layers_to_policys':
            association = self.motor.get_all_association_layer_to_police().to_dict(orient='records')
        else:
            association = self.motor.get_all_association_rule_to_layer().to_dict(orient='records')
        return association

    def get_association_by_id(self, path: Union[PathLayersPolicys, PathRulesLayers], type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para buscar todos as associações por id.
        """

        current_app.logger.info('[Association] - executa metodo get_association_by_id')
        if type_association == 'layers_to_policys':
            association = (
                self.motor
                .get_association_layer_to_police_by_id(path.type_id, [path.index_id])
                .sort_values('priority')
                .to_dict(orient='records')
            )
        else:
            association = (
                self.motor
                .get_association_rule_to_layer_by_id(path.type_id, [path.index_id])
                .to_dict(orient='records')
            )
        return association
    
    def delete_association(self, path: PathAssociation, type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para deletar associações por id.
        """

        current_app.logger.info('[Association] - executa metodo delete_association')
        if type_association == 'layers_to_policys':
            association = self.motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
        else:
            association = self.motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
        if len(association):
            data_update = association.copy()
            data_update['status'] = 'inactive'
            data_update.rename(columns={'association_id': 'id'}, inplace=True)
            self.motor.update_item(type_association, data_update.to_dict(orient='records'))
        return association.to_dict(orient='records')

    def associate_layers_to_policys(self, body: BodyAssociationLayersPolicys) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para adicionar nova associação de camada com polítcia.

        Raises:
            SystemError: gera erro quando não é encontrado camada para o id fornecido
            SystemError: gera erro quando não é encontrado política para o id fornecido
        """

        current_app.logger.info('[Association] - executa metodo associate_layers_to_policys')
        policy = self.motor.get_policys_by_id([body.policy_id])
        layer = self.motor.get_layers_by_id([body.layer_id])
        other_layers_association = (
            self.motor
            .get_association_layer_to_police_by_id('policy_id', [body.policy_id])
        )
        if len(policy) and len(layer):
            layers_to_policys = self.motor.get_all_association_layer_to_police(status='inactive')
            layers_to_policys_update = layers_to_policys.query(f'layer_id == {body.layer_id} and policy_id == {body.policy_id}')
            if len(layers_to_policys_update):
                layers_to_policys_update["priority"] = len(other_layers_association)
                layers_to_policys_update['status'] = 'active'
                layers_to_policys_update.rename(columns={'association_id':'id'}, inplace=True)
                self.motor.update_item('layers_to_policys', layers_to_policys_update.to_dict(orient='records'))
                id_save = layers_to_policys_update['id'].to_list()
            else:
                data_save = {
                    'id': None,
                    'policy_id': body.policy_id,
                    'layer_id': body.layer_id,
                    'priority': len(other_layers_association)
                }
                id_save = self.motor.add_item('layers_to_policys', [data_save])
            association_create = (
                self.motor
                .get_association_layer_to_police_by_id('association_id', id_save)
                .to_dict(orient='records')
            )
            return association_create
        if len(policy):
            raise SyntaxError("The specified layer does not exist.")
        raise SyntaxError("The specified policy does not exist.")

    def associate_rules_to_layers(self, body: BodyAssociationRulesLayers) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para adicionar nova associação de regra com camada.

        Raises:
            SystemError: gera erro quando não é encontrado camada para o id fornecido
            SystemError: gera erro quando não é encontrado regra para o id fornecido
        """

        current_app.logger.info('[Association] - executa metodo associate_rules_to_layers')
        layer = self.motor.get_layers_by_id([body.layer_id])
        rule = self.motor.get_rules_by_id([body.rule_id])
        if len(rule) and len(layer):
            rule_to_layer = self.motor.get_all_association_rule_to_layer(status='inactive')
            rule_to_layer_update = rule_to_layer.query(f'layer_id == {body.layer_id} and rule_id == {body.rule_id}')
            if len(rule_to_layer_update): 
                rule_to_layer_update["action"] = body.action
                rule_to_layer_update['status'] = 'active'
                rule_to_layer_update.rename(columns={'association_id': 'id'}, inplace=True)
                self.motor.update_item('rules_to_layers', rule_to_layer_update.to_dict(orient='records'))
                id_save = rule_to_layer_update['id'].to_list()
            else:
                data_save = {
                    'id': None,
                    "layer_id": body.layer_id,
                    "rule_id": body.rule_id,
                    "action": body.action
                }
                id_save = self.motor.add_item('rules_to_layers', [data_save])
            association_create = (
                self.motor
                .get_association_rule_to_layer_by_id('association_id', id_save)
                .to_dict(orient='records')
            )
            return association_create
        elif len(rule):
            raise SyntaxError("The specified layer does not exist.")
        raise SyntaxError("The specified rule does not exist.")

    def alter_priority_layers_to_policys(self, body: BodyPrioritys) -> list[dict]:
        """
        Método responsável por tratar a requisição da API para alterar as prioridades das camadas na Associação Camadas com Política.

        Raises:
            SystemError: gera erro quando é informado mais do que um id de política na requisição
            SystemError: gera erro quando não são informados todas as associações vinculados ao id de política
        """

        current_app.logger.info('[Association] - executa metodo alter_priority_layers_to_policys')
        itens = []
        association_id = []
        
        for item in body.prioritys:
            itens.append(item.model_dump())
            association_id.append(item.association_id)

        association = self.motor.get_all_association_layer_to_police()
        if association.query('association_id in @association_id')['policy_id'].nunique() > 1:
            raise SyntaxError("Sorting can only be done one policy at a time.")
        policy_id = association.query('association_id in @association_id')['policy_id'].unique()
        itens_not_informed = (
            association
            .query('policy_id in @policy_id')
            .query('association_id not in @association_id')['association_id']
            .to_list()
        )
        if itens_not_informed:
            raise SyntaxError("All layer IDs linked to the policy must be provided.")

        prioritys = pd.DataFrame(itens)
        prioritys = prioritys.sort_values(['priority', 'association_id']).reset_index(drop=True)
        prioritys['priority'] = prioritys.index
        self.motor.update_item('layers_to_policys', prioritys.rename(columns={'association_id': 'id'}).to_dict(orient='records'))
        return prioritys.to_dict(orient='records')
    
    def update_rules_to_layers(self, path: PathAssociation, query: QueryUpdateAssociationRulesLayers):     
        """
        Método responsável por tratar a requisição da API de atualização associação de rega com camada.

        Raises:
            SystemError: gera erro para os casos em que o id informado não existe
        """

        current_app.logger.info('[Association] - executa metodo update_rules_to_layers')
        
        previous_association = self.motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
        if len(previous_association):
            data_update = {key: value for key, value in query.model_dump().items() if value is not None}
            data_update['id'] = path.association_id
            self.motor.update_item('rules_to_layers', [data_update])
            update_association = self.motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
            return (
                previous_association.to_dict(orient='records'), 
                update_association.to_dict(orient='records')
            )
        raise SystemError('Association does not exist.')
