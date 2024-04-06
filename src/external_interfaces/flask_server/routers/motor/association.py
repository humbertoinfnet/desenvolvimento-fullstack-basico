import json
import pandas as pd
from typing import Literal, List
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.interface_adapters.request_arxiv.rest_adapters import request_object as res
from src.external_interfaces.database.controllers.motor import Motor


tag = Tag(name="Associações", description="Associações")
blueprint = APIBlueprint('association', __name__, abp_tags=[tag], doc_ui=True)


class QueryAssociationLayersPolicys(BaseModel):
    policy_id: int = Field(..., gt=0, description='origem id')
    layer_id: int = Field(..., gt=0, description='destino id')

class QueryAssociationRulesLayers(BaseModel):
    rule_id: int = Field(..., gt=0, description='origem id')
    layer_id: int = Field(..., gt=0, description='destino id')
    action: Literal['refuse', 'pendency'] = Field(description="Ação que a regra deverá fazer")

class UpdateAssociationRulesLayers(BaseModel):
    action: Literal['refuse', 'pendency'] = Field(description="Ação que a regra deverá fazer")

class PriorityLayersPolicys(BaseModel):
    association_id: int = Field(..., gt=0, description='id referente a associação')
    priority: int = Field(..., ge=0, description='Prioridade da associação')

class BodyPrioritys(BaseModel):
    prioritys: list[PriorityLayersPolicys] = Field(..., description='')

class Path(BaseModel):
    association_id: int = Field(..., gt=0, description='association_id id')

class PathLayersPolicys(BaseModel):
    index_id: int = Field(..., gt=0, description='Número do id')
    type_id: Literal['association_id', 'policy_id', 'layer_id'] = Field(description="Tipo de id para a busca")

class PathRulesLayers(BaseModel):
    index_id: int = Field(..., gt=0, description='Número do id')
    type_id: Literal['association_id', 'layer_id', 'rule_id'] = Field(description="Tipo de id para a busca")


def update_association(path, query, type_association):
    motor = Motor()
    if type_association == 'layers_to_policys':
        association = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
    else:
        association = motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
    if len(association):
        data_update = {key: value for key, value in query.model_dump().items() if value is not None}
        data_update['id'] = path.association_id
        motor.update_item(type_association, [data_update])
        association_update = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
        return Response(
            json.dumps(
                {
                    'msg': 'Associação atualizada com sucesso',
                    'previous': association.to_dict(orient='records'),
                    'updated': association_update.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe associação para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

def delete_association(path: Path, type_association):
    """
    Rota DELETE para deletar as Associações por id
    """
    motor = Motor()
    if type_association == 'layers_to_policys':
        association = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
    else:
        association = motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
    if len(association):
        data_update = association.copy()
        data_update['status'] = 'inactive'
        data_update.rename(columns={'association_id': 'id'}, inplace=True)
        motor.update_item(type_association, data_update.to_dict(orient='records'))
        return Response(
            json.dumps(
                {
                    'msg': 'Associação deletada com sucesso',
                    'deleted': association.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe associação para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )








@blueprint.get('/associate-layers-to-policys')
def get_all_layers_to_policys():
    """
    Rota GET para acessar todas as Associações Camadas com Política
    """
    motor = Motor()
    association = motor.get_all_association_layer_to_police().to_dict(orient='records')
    try:          
        return Response(
            json.dumps(association, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
        
    except:
        return Response(
            json.dumps(
                {
                    'msg': 'erro',
                }
            ),
            mimetype="application/json",
            status=500,
        )

@blueprint.get('/associate-layers-to-policys/<int:index_id><string:type_id>')
def get_layers_to_policys_by_id(path: PathLayersPolicys):
    """
    Rota GET para acessar a Associação Camadas com Política por id
    """
    motor = Motor()
    association = (
        motor
        .get_association_layer_to_police_by_id(path.type_id, [path.index_id])
        .sort_values('priority')
        .to_dict(orient='records')
    )
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/associate-layers-to-policys/<int:association_id>')
def delete_layers_to_policys(path: Path):
    """
    Rota DELETE da Associação Camadas com Política
    """
    return delete_association(path, 'layers_to_policys')

@blueprint.post('/associate-layers-to-policys')
def associate_layers_to_policys(query: QueryAssociationLayersPolicys):
    """
    Rota POST para adicionar nova Associação Camadas com Política
    """
    motor = Motor()
    policy = motor.get_policys_by_id([query.policy_id])
    layer = motor.get_layers_by_id([query.layer_id])
    other_layers_association = (
        motor
        .get_association_layer_to_police_by_id('policy_id', [query.policy_id])
    )
    if policy and layer:
        data_save = {
            'id': None,
            'policy_id': query.policy_id,
            'layer_id': query.layer_id,
            'priority': len(other_layers_association),
            'name_layer': layer[0].get('name'),
            'name_policy': policy[0].get('name'),
        }
        motor.add_item('layers_to_policys', [data_save])
        return Response(
            json.dumps(
                {
                    "message": "Associação realizada com sucesso",
                    "associate": f"Política: {policy[0].get('name')} com Camada: {layer[0].get('name')}"
                }, 
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    elif policy:
        msg = 'Não existe camada para os parâmetros informados'
    else:
        msg = 'Não existe política para os parâmetros informados'
    return Response(
        json.dumps(
            {'msg': msg},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.post('/associate-layers-to-policys/alter-priority')
def alter_priority_layers_to_policys(body: BodyPrioritys):
    """
    Rota POST responsável por alterar as prioridades das camadas na Associação Camadas com Política
    """
    itens = []
    association_id = []
    
    for item in body.prioritys:
        itens.append(item.model_dump())
        association_id.append(item.association_id)

    motor = Motor()
    association = motor.get_all_association_layer_to_police()
    if association.query('association_id in @association_id')['policy_id'].nunique() > 1:
        return Response(
            json.dumps(
                {
                    'msg': 'a ordenacao deve ser feita apenas uma politica por vez'
                }
                , ensure_ascii=False
            ),
            mimetype="application/json",
            status=500,
        )
    policy_id = association.query('association_id in @association_id')['policy_id'].unique()
    itens_not_informed = (
        association
        .query('policy_id in @policy_id')
        .query('association_id not in @association_id')['association_id']
        .to_list()
    )
    if itens_not_informed:
        return Response(
            json.dumps(
                {
                    'association_id_not_informed': itens_not_informed
                }
                , ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )

    prioritys = pd.DataFrame(itens)
    prioritys = prioritys.sort_values(['priority', 'association_id']).reset_index(drop=True)
    prioritys['priority'] = prioritys.index
    motor.update_item('layers_to_policys', prioritys.rename(columns={'association_id': 'id'}).to_dict(orient='records'))
    return Response(
        json.dumps(
            {
                "message": "Prioridades atualizadas com sucesso",
                "prioritys": prioritys.to_dict(orient='records')
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )




@blueprint.get('/associate-rules-to-layers')
def get_rules_to_layers():
    """
    Rota GET para acessar todas as Associações Regras com Camada
    """
    motor = Motor()
    association = motor.get_all_association_rule_to_layer().to_dict(orient='records')
    try:          
        return Response(
            json.dumps(association, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
        
    except:
        return Response(
            json.dumps(
                {
                    'msg': 'erro',
                }
            ),
            mimetype="application/json",
            status=500,
        )

@blueprint.get('/associate-rules-to-layers/<int:index_id><string:type_id>')
def get_rules_to_layers_by_id(path: PathRulesLayers):
    """
    Rota GET para acessar a Associação Regras com Camada por id
    """
    motor = Motor()
    association = (
        motor
        .get_association_rule_to_layer_by_id(path.type_id, [path.index_id])
        .to_dict(orient='records')
    )
    return Response(
        json.dumps(association, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/associate-rules-to-layers/<int:association_id>')
def delete_rules_to_layers(path: Path):
    """
    Rota DELETE da Associação Regras com Camada
    """
    return delete_association(path, 'rules_to_layers')

@blueprint.put('/associate-rules-to-layers/<int:association_id>')
def update_rules_to_layers(path: Path, query: UpdateAssociationRulesLayers):
    """
    Rota PUT para alteração da Ação da regra na Associação Regras com Camada
    """
    return update_association(path, query, 'rules_to_layers')

@blueprint.post('/associate-rules-to-layers')
def associate_rules_to_layers(query: QueryAssociationRulesLayers):
    """
    Rota POST para adicionar nova Associação Regras com Camada
    """
    motor = Motor()
    layer = motor.get_layers_by_id([query.layer_id])
    rule = motor.get_rules_by_id([query.rule_id])
    if rule and layer:
        data_save = {
            'id': None,
            "layer_id": query.layer_id,
            "rule_id": query.rule_id,
            "action": query.action,
            "name_layer": layer[0].get('name'),
            "name_rule": rule[0].get('name'),
        }
        motor.add_item('rules_to_layers', [data_save])
        return Response(
            json.dumps(
                {
                    "message": "Associação realizada com sucesso",
                    "associate": f"Camada: {layer[0].get('name')} com Regra: {rule[0].get('name')}"
                }, 
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    elif rule:
        msg = 'Não existe camada para os parâmetros informados'
    else:
        msg = 'Não existe regra para os parâmetros informados'
    return Response(
        json.dumps(
            {'msg': msg},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )