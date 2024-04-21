from dataclasses import dataclass
from flask import current_app
from src.interface_adapters.database.controllers.motor import Motorinterface
from .update_association import UpdateAssociation
from src.interface_adapters.schemas.motor.policys import (
    BodyPolicy
)


@dataclass
class Policys:
    """
    Método responsável pela lógica envolvendo o elemento de politicas.
    """

    motor: Motorinterface
    update_association: UpdateAssociation

    def get_policys(self) -> list:
        """
        Método responsável por tratar a requisição da API para buscar todas as políticas.
        """

        current_app.logger.info('[Policys] - executa metodo get_policys')
        policys = self.motor.get_all_policys().to_dict(orient='records')
        return policys
    
    def get_policy_by_id(self, policy_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para buscar política por id.
        """

        current_app.logger.info('[Policys] - executa metodo get_policy_by_id')
        policy = self.motor.get_policys_by_id([policy_id]).to_dict(orient='records')
        return policy
    
    def update_policy(self, policy_id: int, values_input: dict) -> tuple:
        """
        Método responsável por tratar a requisição da API para atualizar política por id.
        """

        current_app.logger.info('[Policys] - executa metodo update_policy')
        previous_policy = self.motor.get_policys_by_id([policy_id])
        if len(previous_policy):
            data_update = {key: value for key, value in values_input.items() if value is not None}
            data_update['id'] = policy_id
            self.motor.update_item('policys', [data_update])
            updated_policy = self.motor.get_policys_by_id([policy_id])
            return previous_policy.to_dict(orient='records'), updated_policy.to_dict(orient='records')
        return previous_policy.to_dict(orient='records'), {}

    def delete_policy(self, policy_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para excluir política por id.
        """

        current_app.logger.info('[Policys] - executa metodo delete_policy')
        policy = self.motor.get_policys_by_id([policy_id])
        if len(policy):
            data_update = [{'id': policy_id, 'status': 'inactive'}]
            self.motor.update_item('policys', data_update)
            self.update_association.update_association_policys_to_layers(policy_id, 'policy_id')
        return policy.to_dict(orient='records')

    def add_policy(self, body: BodyPolicy) -> dict:
        """
        Método responsável por tratar a requisição da API para adicionar nova política.
        """

        current_app.logger.info('[Policys] - executa metodo add_policy')
        policys = self.motor.get_all_policys(status='inactive')
        policy_update = policys.query(f'name == "{body.name}"')
        if len(policy_update):
            policy_update['name'] = body.name
            policy_update['description'] = body.description
            policy_update['status'] = 'active'
            policy_update.rename(columns={'policy_id':'id'}, inplace=True)
            self.motor.update_item('policys', policy_update.to_dict(orient='records'))
            id_save = policy_update['id'].to_list()
        else:
            data_save = body.model_dump().copy()
            data_save['id'] = None
            id_save = self.motor.add_item('policys', [data_save])
        data_create = body.model_dump().copy()
        data_create['policy_id'] = id_save[0]
        data_create['identify'] = 'policys'
        return data_create
