
from flask import current_app, Response, json
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.use_cases.motor import MotorConfig, UpdateAssociation
from src.interface_adapters.schemas.motor.rules import (
    PathRule,
    BodyRule,
    ResponseSuccessRule,
    ResponseSuccessRuleDelete,
    ResponseSuccessRuleUpdate,
    ResponseSuccessRuleAdd
)
from src.interface_adapters.schemas.response import (
    ResponseError,
    ResponseSuccess,
    ResponseNoContent
)


tag = Tag(name="Regras", description="Rotas para controle das Regras")
blueprint = APIBlueprint(
    'Regras',
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
    '/rules',
    responses={200: ResponseSuccessRule}
)
def get_rules():
    """
    Rota GET para acessar todas as Regras
    """

    current_app.logger.info('[route-rules] - acessa a rota GET /rules')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rules = motor_config.rules.get_rules()
    return Response(
        json.dumps(rules, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.get(
    '/rule/<int:rule_id>',
    responses={200: ResponseSuccessRule}
)
def get_rule_by_id(path: PathRule):
    """
    Rota GET para acessar as Regras por id
    """

    current_app.logger.info('[route-rules] - acessa a rota GET /rule/{rule_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rules = motor_config.rules.get_rule_by_id(path.rule_id)
    if len(rules):
        return Response(
            json.dumps(rules, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
    return Response(
        mimetype="application/json",
        status=204,
    )


@blueprint.delete(
    '/rule/<int:rule_id>',
    responses={200: ResponseSuccessRuleDelete}
)
def delete_rule_by_id(path: PathRule):
    """
    Rota DELETE das Regras por id
    """

    current_app.logger.info('[route-rules] - acessa a rota DELETE /rule/{rule_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.rules.delete_rule(path.rule_id)
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
    '/rule/<int:rule_id>',
    responses={200: ResponseSuccessRuleUpdate}
)
def update_rule(path: PathRule, query: BodyRule):
    """
    Rota PUT para atualização de Regra por id
    """

    current_app.logger.info('[route-rules] - acessa a rota PUT /rule/{rule_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    previous_rule, updated_rule = motor_config.rules.update_rule(path.rule_id, query.model_dump())
    if len(previous_rule):
        return Response(
            json.dumps(
                {
                    'message': 'success_updated',
                    'previous': previous_rule,
                    'updated': updated_rule
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
    '/rule',
    responses={200: ResponseSuccessRuleAdd}
)
def add_rule(body: BodyRule):
    """
    Rota POST para adicionar Nova Regra
    """

    current_app.logger.info('[route-rules] - acessa a rota POST /rule')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rule_create = motor_config.rules.add_rule(body)
    return Response(
        json.dumps(
            {
                "message": "success_add",
                "create": rule_create
            },
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
