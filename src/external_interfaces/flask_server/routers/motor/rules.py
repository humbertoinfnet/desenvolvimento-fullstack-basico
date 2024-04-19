
from flask import request, Response, json
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
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rules = motor_config.rule.get_rules()
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
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rules = motor_config.rule.get_rule_by_id(path.rule_id)
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
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.rule.delete_rule(path.rule_id)
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
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    previous_rule, updated_rule = motor_config.rule.update_rule(path.rule_id, query.model_dump())
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
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    rule_create = motor_config.rule.add_rule(body)
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
