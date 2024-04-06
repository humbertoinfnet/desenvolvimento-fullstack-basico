import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.interface_adapters.request_arxiv.rest_adapters import request_object as res


tag = Tag(name="Politicas", description="Politicas")
blueprint = APIBlueprint('politicas', __name__, abp_tags=[tag], doc_ui=True)


class BookBody(BaseModel):
    age: Optional[int] = Field(..., ge=2, le=4, description='Age')
    author: str = Field(None, min_length=2, max_length=4, description='Author')


class BookQuery(BaseModel):
    type: str

class Path(BaseModel):
    policy_id: int = Field(..., description='Policy id')

class PolicyBody(BaseModel):
    name: Optional[str] = Field(None, description='Nome da política')
    description: Optional[str] = Field(None, description='Descrição da política')


@blueprint.get('/policys')
def get_policys():
    """
    Rota GET para acessar todas as Políticas
    """

    motor = Motor()
    policys = motor.get_all_policys().to_dict(orient='records')
    try:          
        return Response(
            json.dumps(policys, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
        
    except:
        return Response(
            json.dumps({'msg': 'erro'}),
            mimetype="application/json",
            status=500,
        )

@blueprint.get('/policy/<int:policy_id>')
def get_policy_by_id(path: Path):
    """
    Rota GET para acessar as Politicas por id
    """
    motor = Motor()
    policy = motor.get_policys_by_id([path.policy_id]).to_dict(orient='records')
    return Response(
        json.dumps(policy, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/policy/<int:policy_id>')
def delete_policy_by_id(path: Path):
    """
    Rota DELETE das Políticas por id
    """
    motor = Motor()
    policy = motor.get_policys_by_id([path.policy_id])
    if len(policy):
        data_update = [{'id': path.policy_id, 'status': 'inactive'}]
        motor.update_item('policys', data_update)
        return Response(
            json.dumps(
                {
                    'msg': 'Política deletada com sucesso',
                    'deleted': policy.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe política para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.put('/policy/<int:policy_id>')
def update_policy(path: Path, query: PolicyBody):
    """
    Rota PUT para atualização de Politica por id
    """
    motor = Motor()
    previous_policy = motor.get_policys_by_id([path.policy_id])
    if len(previous_policy):
        data_update = {key: value for key, value in query.model_dump().items() if value is not None}
        data_update['id'] = path.policy_id
        motor.update_item('policys', [data_update])
        updated_policy = motor.get_policys_by_id([path.policy_id])
        return Response(
            json.dumps(
                {
                    'msg': 'Política atualizada com sucesso',
                    'previous': previous_policy.to_dict(orient='records'),
                    'updated': updated_policy.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe política para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.post('/policy')
def add_policy(body: PolicyBody):
    """
    Rota POST para adicionar Nova Politica
    """
    motor = Motor()
    data_save = body.model_dump().copy()
    data_save['id'] = None
    motor.add_item('policys', [data_save])
    return Response(
        json.dumps(
            {
                "message": "Política inserida com sucesso",
                "policy": body.model_dump()
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
