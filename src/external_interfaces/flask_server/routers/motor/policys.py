from flask import request, Response, current_app, json
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.use_cases.motor import MotorConfig, UpdateAssociation
from src.interface_adapters.schemas.motor.policys import (
    BodyPolicy,
    PathPolicy,
    ResponseSuccessPolicy,
    ResponseSuccessPolicyAdd,
    ResponseSuccessPolicyDelete,
    ResponseSuccessPolicyUpdate
)
from src.interface_adapters.schemas.response import (
    ResponseError,
    ResponseSuccess,
    ResponseNoContent
)

tag = Tag(name="Politicas", description="Rotas para controle das Políticas")
blueprint = APIBlueprint(
    'politicas',
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
    '/policys',
    responses={200: ResponseSuccessPolicy}
)
def get_policys():
    """
    Rota GET para acessar todas as Políticas
    """

    current_app.logger.info('[route-layers] - acessa a rota GET /policys')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    policys = motor_config.policys.get_policys()
    return Response(
        json.dumps(policys, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.get(
    '/policy/<int:policy_id>',
    responses={200: ResponseSuccessPolicy}
)
def get_policy_by_id(path: PathPolicy):
    """
    Rota GET para acessar as Politicas por id
    """

    current_app.logger.info('[route-layers] - acessa a rota GET /policy/{policy_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    policys = motor_config.policys.get_policy_by_id(path.policy_id)
    if len(policys):
        return Response(
            json.dumps(policys, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
    return Response(
        mimetype="application/json",
        status=204,
    )


@blueprint.delete(
    '/policy/<int:policy_id>',
    responses={200: ResponseSuccessPolicyDelete}
)
def delete_policy_by_id(path: PathPolicy):
    """
    Rota DELETE das Políticas por id
    """

    current_app.logger.info('[route-layers] - acessa a rota DELETE /policy/{policy_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.policys.delete_policy(path.policy_id)
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
    '/policy/<int:policy_id>',
    responses={200: ResponseSuccessPolicyUpdate}
)
def update_policy(path: PathPolicy, query: BodyPolicy):
    """
    Rota PUT para atualização de Politica por id
    """

    current_app.logger.info('[route-layers] - acessa a rota PUT /policy/{policy_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    previous_policys, updated_policys = (
        motor_config
        .policys
        .update_policy(path.policy_id, query.model_dump())
    )
    if len(previous_policys):
        return Response(
            json.dumps(
                {
                    'message': 'success_updated',
                    'previous': previous_policys,
                    'updated': updated_policys
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
    '/policy',
    responses={200: ResponseSuccessPolicyAdd}
)
def add_policy(body: BodyPolicy):
    """
    Rota POST para adicionar Nova Politica
    """

    current_app.logger.info('[route-layers] - acessa a rota POST /policy')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    policy_create = motor_config.policys.add_policy(body)
    return Response(
        json.dumps(
            {
                "message": "success_add",
                "create": policy_create
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
