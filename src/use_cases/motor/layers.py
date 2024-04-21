from dataclasses import dataclass
from flask import current_app
from src.interface_adapters.database.controllers.motor import Motorinterface
from .update_association import UpdateAssociation
from src.interface_adapters.schemas.motor.layers import (
    BodyLayer
)


@dataclass
class Layers:
    """
    Método responsável pela lógica envolvendo o elemento de camadas.
    """

    motor: Motorinterface
    update_association: UpdateAssociation

    def get_layers(self) -> list:
        """
        Método responsável por tratar a requisição da API para buscar todas as camadas.
        """

        current_app.logger.info('[Layers] - executa metodo get_layers')
        layers = self.motor.get_all_layers().to_dict(orient='records')
        return layers
    
    def get_layer_by_id(self, layer_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para buscar camada por id.
        """

        current_app.logger.info('[Layers] - executa metodo get_layer_by_id')
        layer = self.motor.get_layers_by_id([layer_id]).to_dict(orient='records')
        return layer
    
    def update_layer(self, layer_id: int, values_input: dict) -> tuple:
        """
        Método responsável por tratar a requisição da API para atualizar camada por id.
        """

        current_app.logger.info('[Layers] - executa metodo update_layer')
        previous_layer = self.motor.get_layers_by_id([layer_id])
        if len(previous_layer):
            data_update = {key: value for key, value in values_input.items() if value is not None}
            data_update['id'] = layer_id
            self.motor.update_item('layers', [data_update])
            updated_layer = self.motor.get_layers_by_id([layer_id])
            return previous_layer.to_dict(orient='records'), updated_layer.to_dict(orient='records')
        return previous_layer.to_dict(orient='records'), {}

    def delete_layer(self, layer_id: int) -> list:
        """
        Método responsável por tratar a requisição da API para excluir camada por id.
        """

        current_app.logger.info('[Layers] - executa metodo delete_layer')
        layer = self.motor.get_layers_by_id([layer_id])
        if len(layer):
            data_update = [{'id': layer_id, 'status': 'inactive'}]
            self.motor.update_item('layers', data_update)
            self.update_association.update_association_rules_to_layers(layer_id, 'layer_id')
            self.update_association.update_association_policys_to_layers(layer_id, 'layer_id')
        return layer.to_dict(orient='records')

    def add_layer(self, body: BodyLayer) -> dict:
        """
        Método responsável por tratar a requisição da API para adicionar nova camada.
        """

        current_app.logger.info('[Layers] - executa metodo add_layer')
        layers = self.motor.get_all_layers(status='inactive')
        layer_update = layers.query(f'name == "{body.name}"')
        if len(layer_update):
            layer_update['name'] = body.name
            layer_update['description'] = body.description
            layer_update['status'] = 'active'
            layer_update.rename(columns={'layer_id': 'id'}, inplace=True)
            self.motor.update_item('layers', layer_update.to_dict(orient='records'))
            id_save = layer_update['id'].to_list()
        else:
            data_save = body.model_dump().copy()
            data_save['id'] = None
            id_save = self.motor.add_item('layers', [data_save])
        data_create = body.model_dump().copy()
        data_create['layer_id'] = id_save[0]
        data_create['identify'] = 'layers'
        return data_create
