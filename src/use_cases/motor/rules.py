from dataclasses import dataclass
from flask import current_app
from src.interface_adapters.database.controllers.motor import Motorinterface
from .update_association import UpdateAssociation
from src.interface_adapters.schemas.motor.rules import (
    BodyRule
)


@dataclass
class Rules:
    """
    Método responsável pela lógica envolvendo o elemento de regras.
    """

    motor: Motorinterface
    update_association: UpdateAssociation

    def get_rules(self) -> list:
        """
        Método responsável por tratar a requisição da API para buscar todas as regras.
        """

        current_app.logger.info('[Rules] - executa metodo get_rules')
        rules = self.motor.get_all_rules().to_dict(orient='records')
        return rules
    
    def get_rule_by_id(self, rule_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para buscar regra por id.
        """

        current_app.logger.info('[Rules] - executa metodo get_rule_by_id')
        rule = self.motor.get_rules_by_id([rule_id]).to_dict(orient='records')
        return rule
    
    def update_rule(self, rule_id: int, values_input: dict) -> tuple:
        """
        Método responsável por tratar a requisição da API para atualizar regra por id.
        """

        current_app.logger.info('[Rules] - executa metodo update_rule')
        previous_rule = self.motor.get_rules_by_id([rule_id])
        if len(previous_rule):
            data_update = {key: value for key, value in values_input.items() if value is not None}
            data_update['id'] = rule_id
            self.motor.update_item('rules', [data_update])
            updated_rule = self.motor.get_rules_by_id([rule_id])
            return previous_rule.to_dict(orient='records'), updated_rule.to_dict(orient='records')
        return previous_rule.to_dict(orient='records'), {}

    def delete_rule(self, rule_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para excluir regra por id.
        """

        current_app.logger.info('[Rules] - executa metodo delete_rule')
        rule = self.motor.get_rules_by_id([rule_id])
        if len(rule):
            data_update = [{'id': rule_id, 'status': 'inactive'}]
            self.motor.update_item('rules', data_update)
            self.update_association.update_association_rules_to_layers(rule_id, 'rule_id')
        return rule.to_dict(orient='records')

    def add_rule(self, body: BodyRule) -> dict:
        """
        Método responsável por tratar a requisição da API para adicionar nova regra.
        """

        current_app.logger.info('[Rules] - executa metodo add_rule')
        rules = self.motor.get_all_rules(status='inactive')
        rule_update = rules.query(f'name == "{body.name}"')
        if len(rule_update):
            rule_update['name'] = body.name
            rule_update['code'] = body.code
            rule_update['rule'] = body.rule
            rule_update['description'] = body.description
            rule_update['status'] = 'active'
            rule_update.rename(columns={'rule_id': 'id'}, inplace=True)
            self.motor.update_item('rules', rule_update.to_dict(orient='records'))
            id_save = rule_update['id'].to_list()
        else:
            data_save = body.model_dump().copy()
            data_save['id'] = None
            id_save = self.motor.add_item('rules', [data_save])
        data_create = body.model_dump().copy()
        data_create['rule_id'] = id_save[0]
        data_create['identify'] = 'rules'
        return data_create
