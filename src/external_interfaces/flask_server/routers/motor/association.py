from flask import Response, current_app, json
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.use_cases.motor import MotorConfig, UpdateAssociation
from src.interface_adapters.schemas.motor.association import (
    PathLayersPolicys,
    PathRulesLayers,
    BodyAssociationLayersPolicys,
    BodyAssociationRulesLayers,
    BodyPrioritys,
    QueryUpdateAssociationRulesLayers,
    PathAssociation,
    ResponseSuccessAssociationLayersPolicys,
    ResponseSuccessAssociationRulesLayers,
    ResponseSuccessAssociationLayersPolicysAdd,
    ResponseSuccessAssociationLayersPolicysDelete,
    ResponseSuccessAssociationLayersPolicysUpdate,
    ResponseSuccessAssociationRulesLayersAdd,
    ResponseSuccessAssociationRulesLayersDelete,
    ResponseSuccessAssociationRulesLayersUpdate
)
from src.interface_adapters.schemas.response import (
    ResponseError,
    ResponseSuccess,
    ResponseNoContent
)


tag = Tag(name="Associações", description="Rotas para controle das Associações")
blueprint = APIBlueprint(
    'association',
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
    '/associate-layers-to-policys',
    responses={200: ResponseSuccessAssociationLayersPolicys}
)
def get_all_layers_to_policys() -> Response:
    """
    Rota GET para acessar todas as Associações Camadas com Política
    """
    current_app.logger.info('[route-association] - acessa a rota GET /associate-layers-to-policys')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association = motor_config.association.get_all_association('layers_to_policys')
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.get(
    '/associate-layers-to-policys/<int:index_id><string:type_id>',
    responses={200: ResponseSuccessAssociationLayersPolicys}
)
def get_layers_to_policys_by_id(path: PathLayersPolicys) -> Response:
    """
    Rota GET para acessar a Associação Camadas com Política por id
    """

    current_app.logger.info('[route-association] - acessa a rota GET /associate-layers-to-policys/{index_id}{type_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association = motor_config.association.get_association_by_id(path, 'layers_to_policys')
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.delete(
    '/associate-layers-to-policys/<int:association_id>',
    responses={200: ResponseSuccessAssociationLayersPolicysDelete}
)
def delete_layers_to_policys(path: PathAssociation) -> Response:
    """
    Rota DELETE da Associação Camadas com Política
    """

    current_app.logger.info('[route-association] - acessa a rota DELETE /associate-layers-to-policys/{association_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.association.delete_association(path, 'layers_to_policys')
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


@blueprint.post(
    '/associate-layers-to-policys',
    responses={200: ResponseSuccessAssociationLayersPolicysAdd}
)
def associate_layers_to_policys(body: BodyAssociationLayersPolicys) -> Response:
    """
    Rota POST para adicionar nova Associação Camadas com Política
    """

    current_app.logger.info('[route-association] - acessa a rota POST /associate-layers-to-policys')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association_create = motor_config.association.associate_layers_to_policys(body)
    return Response(
        json.dumps(
            {
                "message": "success_add",
                "create": association_create
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )


@blueprint.post(
    '/associate-layers-to-policys/alter-priority',
    responses={200: ResponseSuccessAssociationLayersPolicysUpdate}
)
def alter_priority_layers_to_policys(body: BodyPrioritys) -> Response:
    """
    Rota POST responsável por alterar as prioridades das camadas na Associação Camadas com Política
    """

    current_app.logger.info('[route-association] - acessa a rota POST /associate-layers-to-policys/alter-priority')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association_update = motor_config.association.alter_priority_layers_to_policys(body)
    return Response(
        json.dumps(
            {
                "message": "success_updated",
                "prioritys": association_update
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )


@blueprint.get(
    '/associate-rules-to-layers',
    responses={200: ResponseSuccessAssociationRulesLayers}
)
def get_rules_to_layers() -> Response:
    """
    Rota GET para acessar todas as Associações Regras com Camada
    """

    current_app.logger.info('[route-association] - acessa a rota GET /associate-rules-to-layers')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association = motor_config.association.get_all_association('rules_to_layers')
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.get(
    '/associate-rules-to-layers/<int:index_id><string:type_id>',
    responses={200: ResponseSuccessAssociationRulesLayers}
)
def get_rules_to_layers_by_id(path: PathRulesLayers) -> Response:
    """
    Rota GET para acessar a Associação Regras com Camada por id
    """

    current_app.logger.info('[route-association] - acessa a rota GET /associate-rules-to-layers/{index_id}{type_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association = motor_config.association.get_association_by_id(path, 'rules_to_layers')
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.delete(
    '/associate-rules-to-layers/<int:association_id>',
    responses={200: ResponseSuccessAssociationRulesLayersDelete}
)
def delete_rules_to_layers(path: PathAssociation) -> Response:
    """
    Rota DELETE da Associação Regras com Camada
    """

    current_app.logger.info('[route-association] - acessa a rota DELETE /associate-rules-to-layers/{association_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    deleted = motor_config.association.delete_association(path, 'rules_to_layers')
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
    '/associate-rules-to-layers/<int:association_id>',
    responses={200: ResponseSuccessAssociationRulesLayersUpdate}
)
def update_rules_to_layers(path: PathAssociation, query: QueryUpdateAssociationRulesLayers) -> Response:
    """
    Rota PUT para alteração da Ação da regra na Associação Regras com Camada
    """

    current_app.logger.info('[route-association] - acessa a rota PUT /associate-rules-to-layers/{association_id}')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    previous_association, update_association = motor_config.association.update_rules_to_layers(path, query)
    
    return Response(
        json.dumps(
            {
                'msg': 'Associação atualizada com sucesso',
                'previous': previous_association,
                'updated': update_association
            },
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )


@blueprint.post(
    '/associate-rules-to-layers',
    responses={200: ResponseSuccessAssociationRulesLayersAdd}
)
def associate_rules_to_layers(body: BodyAssociationRulesLayers) -> Response:
    """
    Rota POST para adicionar nova Associação Regras com Camada
    """

    current_app.logger.info('[route-association] - acessa a rota POST /associate-rules-to-layers')
    motor = Motor()
    update_association = UpdateAssociation(motor)
    motor_config = MotorConfig(motor, update_association)
    association_create = motor_config.association.associate_rules_to_layers(body)
    return Response(
        json.dumps(
            {
                "message": "success_add",
                "create": association_create
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
