from flask import request, Response, current_app, json
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.use_cases.motor import MotorConfig, UpdateAssociation
from src.interface_adapters.schemas.motor.layers import (
    PathLayer,
    BodyLayer,
    ResponseSuccessLayer,
    ResponseSuccessLayerAdd,
    ResponseSuccessLayerDelete,
    ResponseSuccessLayerUpdate
)
from src.interface_adapters.schemas.response import (
    ResponseError,
    ResponseSuccess,
    ResponseNoContent
)

tag = Tag(name="Camadas", description="Rotas para controle das Camadas")
blueprint = APIBlueprint(
    'layers',
    __name__,
    abp_tags=[tag],
    doc_ui=True,
    abp_responses={
        200: ResponseSuccess,
        204: ResponseNoContent,
        500: ResponseError
    }
)


@blueprint.get(
    '/layers',
    responses={200: ResponseSuccessLayer}
)
def get_layers() -> Response:
    """
    Rota GET para acessar todas as Camadas
    """

    current_app.logger.info('[route-layers] - acessa a rota GET /layers')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    layers = motor_config.layers.get_layers()
    return Response(
        json.dumps(layers, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.get(
    '/layer/<int:layer_id>',
    responses={200: ResponseSuccessLayer}
)
def get_layer_by_id(path: PathLayer) -> Response:
    """
    Rota GET para acessar as Camadas por id
    """
    
    current_app.logger.info('[route-layers] - acessa a rota GET /layer/{layer_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    layers = motor_config.layers.get_layer_by_id(path.layer_id)
    if len(layers):
        return Response(
            json.dumps(layers, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
    return Response(
        mimetype="application/json",
        status=204,
    )


@blueprint.delete(
    '/layer/<int:layer_id>',
    responses={200: ResponseSuccessLayerDelete}
)
def delete_layer_by_id(path: PathLayer) -> Response:
    """
    Rota DELETE das Camadas por id
    """

    current_app.logger.info('[route-layers] - acessa a rota DELETE /layer/{layer_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.layers.delete_layer(path.layer_id)
    if len(deleted):
        return Response(
            json.dumps(
                {
                    'message': 'success_deleted',
                    'deleted': deleted
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        mimetype="application/json",
        status=204,
    )


@blueprint.put(
    '/layer/<int:layer_id>',
    responses={200: ResponseSuccessLayerUpdate}
)
def update_layer(path: PathLayer, query: BodyLayer) -> Response:
    """
    Rota PUT para atualização de Camada por id
    """

    current_app.logger.info('[route-layers] - acessa a rota PUT /layer/{layer_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    previous_layers, updated_layers = (
        motor_config
        .layers
        .update_layer(path.layer_id, query.model_dump())
    )
    if len(previous_layers):
        return Response(
            json.dumps(
                {
                    'message': 'success_updated',
                    'previous': previous_layers,
                    'updated': updated_layers
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        mimetype="application/json",
        status=204,
    )


@blueprint.post(
    '/layer',
    responses={200: ResponseSuccessLayerAdd}
)
def add_layer(body: BodyLayer) -> Response:
    """
    Rota POST para adicionar Nova Camada
    """

    current_app.logger.info('[route-layers] - acessa a rota POST /layer')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    layer_create = motor_config.layers.add_layer(body)
    return Response(
        json.dumps(
            {
                "message": "success_add",
                "create": layer_create
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
