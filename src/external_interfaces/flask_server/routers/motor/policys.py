import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint



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
    name: Optional[str] = Field(None, description='Nome da regra')
    type: Optional[str] = Field(None, description='Lógica da regra')
    description: Optional[str] = Field(None, description='Descrição da regra')


policys = [
    {
        'id': 0,
        'name': 'CARTAO_PJ',
        'type': 'policy',
        'description': 'Política de Cartão para documentos PJ'
    },
    {
        'id': 1,
        'name': 'CARTAO_PF',
        'type': 'policy',
        'description': 'Política de Cartão para documentos PF'
    },
    {
        'id': 2,
        'name': 'ANTECIPACAO_CEDENTE',
        'type': 'policy',
        'description': 'Política de Cedente para o produto antecipação de recebíveis '
    }
    
]

@blueprint.get('/policys')
def get_policys():
    """
    Rota GET para acessar as políticas e camadas cadastradas
    """

    try:         
        return Response(
            json.dumps(policys),
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

@blueprint.get('/policy/<int:policy_id>')
def get_policy_by_id(path: Path):
    """
    Rota GET para acessar as Politicas cadastradas por id
    """
    return Response(
        json.dumps(
            {
                'msg': 'Policy',
                'policy': policys[path.policy_id]
            }
        ),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/policy/<int:policy_id>')
def delete_policy_by_id(path: Path):
    """
    Rota DELETE para deletar as Politicas cadastradas por id
    """
    return Response(
        json.dumps(
            {
                'msg': 'Policy',
                'policy': policys[path.policy_id]
            }
        ),
        mimetype="application/json",
        status=200,
    )

@blueprint.put('/policys/<int:policy_id>')
def update_policy(path: Path, query: PolicyBody):
    """
    Rota para atualização de Politica
    """
    for key, value in query.model_dump().items():
        if value is not None:
            policys[path.policy_id][key] = value
    return json.dumps(policys[path.policy_id], ensure_ascii=False)

@blueprint.post('/policys')
def add_policy(body: PolicyBody):
    """
    Rota para adicionar Nova Politica
    """
    policys.append(body.model_dump())
    return json.dumps({"message": "ok", "policy": body.model_dump()}, ensure_ascii=False)
