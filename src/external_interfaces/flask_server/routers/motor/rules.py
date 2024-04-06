
import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.external_interfaces.database.controllers.motor import Motor
from src.interface_adapters.request_arxiv.rest_adapters import request_object as res


tag = Tag(name="Regras", description="Regras")
blueprint = APIBlueprint('Regras', __name__, abp_tags=[tag], doc_ui=True)


class BookQuery(BaseModel):
    type: str

class Path(BaseModel):
    rule_id: int = Field(..., description='rule id')

class RuleBody(BaseModel):
    name: Optional[str] = Field(None, description='Nome da regra')
    code: Optional[str] = Field(None, description='Código da regra')
    rule: Optional[str] = Field(None, description='Lógica da regra')
    description: Optional[str] = Field(None, description='Descrição da regra')


@blueprint.get('/rules')
def get_rules():
    """
    Rota GET para acessar todas as Regras
    """

    motor = Motor()
    rules = motor.get_all_rules().to_dict(orient='records')
    try:          
        return Response(
            json.dumps(rules, ensure_ascii=False),
            mimetype="application/json",
            status=200,
        )
        
    except:
        return Response(
            json.dumps({'msg': 'erro'}),
            mimetype="application/json",
            status=500,
        )

@blueprint.get('/rule/<int:rule_id>')
def get_rule_by_id(path: Path):
    """
    Rota GET para acessar as Regras por id
    """
    motor = Motor()
    rule = motor.get_rules_by_id([path.rule_id]).to_dict(orient='records')
    return Response(
        json.dumps(rule, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/rule/<int:rule_id>')
def delete_rule_by_id(path: Path):
    """
    Rota DELETE das Regras por id
    """
    motor = Motor()
    rule = motor.get_rules_by_id([path.rule_id])
    if len(rule):
        data_update = [{'id': path.rule_id, 'status': 'inactive'}]
        motor.update_item('rules', data_update)
        return Response(
            json.dumps(
                {
                    'msg': 'Regras deletada com sucesso',
                    'deleted': rule.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe regra para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.put('/rule/<int:rule_id>')
def update_rule(path: Path, query: RuleBody):
    """
    Rota PUT para atualização de Regra por id
    """
    motor = Motor()
    previous_rule = motor.get_rules_by_id([path.rule_id])
    if len(previous_rule):
        data_update = {key: value for key, value in query.model_dump().items() if value is not None}
        data_update['id'] = path.rule_id
        motor.update_item('rules', [data_update])
        updated_rule = motor.get_rules_by_id([path.rule_id])
        return Response(
            json.dumps(
                {
                    'msg': 'Regra atualizada com sucesso',
                    'previous': previous_rule.to_dict(orient='records'),
                    'updated': updated_rule.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe regra para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.post('/rule')
def add_rule(body: RuleBody):
    """
    Rota POST para adicionar Nova Regra
    """
    motor = Motor()
    data_save = body.model_dump().copy()
    data_save['id'] = None
    motor.add_item('rules', [data_save])
    return Response(
        json.dumps(
            {
                "message": "Regra inserida com sucesso",
                "rule": body.model_dump()
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
