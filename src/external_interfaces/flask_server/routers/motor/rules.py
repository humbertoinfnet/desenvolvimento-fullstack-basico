
import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.interface_adapters.request_arxiv.rest_adapters import request_object as res


tag = Tag(name="Regras", description="Regras")
blueprint = APIBlueprint('Regras', __name__, abp_tags=[tag], doc_ui=True)


class BookQuery(BaseModel):
    type: str

class Path(BaseModel):
    rule_id: int = Field(..., description='rule id')

class RuleBody(BaseModel):
    name: Optional[str] = Field(None, description='Nome da regra')
    rule: Optional[str] = Field(None, description='Lógica da regra')
    description: Optional[str] = Field(None, description='Descrição da regra')


rules = [
    {
        'id': 0,
        'name': 'PF_REP001-TempoConta',
        'code': 'REP001',
        'type': 'rule',
        'rule': 'TempoConta > 30',
        'descrição': 'Regra de PF para tempo de conta mínimo em dias'
    },
    {
        'id': 1,
        'name': 'PF_REP002-Idade',
        'code': 'REP002',
        'type': 'rule',
        'rule': 'Idade >= 18 and Idade < 90',
        'descrição': 'Regra de PF para idade no intervalo de 18 a 90'
    },
    {
        'id': 2,
        'name': 'PF_REP003-ScoreSerasa',
        'code': 'REP003',
        'type': 'rule',
        'rule': 'ScoreSerasa > 500',
        'descrição': 'Regra de PF para score serasa maior que 500'
    },
    
]


@blueprint.get('/rules')
def get_rules(query: BookQuery):
    """
    Rota GET para acessar todas as regras cadastradas
    """

    try:
        if query.type == 'rules':
            return Response(
                json.dumps(rules),
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


@blueprint.get('/rules/<int:rule_id>')
def get_rule_by_id(path: Path):
    """
    Rota GET para acessar as regras cadastradas por id
    """
    return Response(
        json.dumps(rules[path.rule_id]),
        mimetype="application/json",
        status=200,
    )


@blueprint.delete('/rules/<int:rule_id>')
def delete_rule_by_id(path: Path):
    """
    Rota DELETE para excluir regras
    """
    return Response(
        json.dumps(rules[path.rule_id]),
        mimetype="application/json",
        status=200,
    )


@blueprint.put('/rules/<int:rule_id>')
def update_rule(path: Path, query: RuleBody):
    """
    Rota para atualização de regra
    """
    for key, value in query.model_dump().items():
        if value is not None:
            rules[path.rule_id][key] = value
    return Response(
        json.dumps(rules[path.rule_id], ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )


@blueprint.post('/rules')
def add_policy(body: RuleBody):
    """
    Rota para adicionar Nova Regra
    """
    rules.append(body.model_dump())
    return Response(
        json.dumps(body.model_dump(), ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )
