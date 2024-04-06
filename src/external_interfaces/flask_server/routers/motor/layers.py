import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.interface_adapters.request_arxiv.rest_adapters import request_object as res
from src.external_interfaces.database.controllers.motor import Motor


tag = Tag(name="Camadas", description="Camadas")
blueprint = APIBlueprint('layers', __name__, abp_tags=[tag], doc_ui=True)


class Query(BaseModel):
    origin_id: int = Field(..., description='origem id')
    destino_id: int = Field(..., description='destino id')

class BookQuery(BaseModel):
    type: str

class Path(BaseModel):
    layer_id: int = Field(..., description='layer id')

class LayerBody(BaseModel):
    name: Optional[str] = Field(None, description='Nome da camada')
    description: Optional[str] = Field(None, description='Descrição da camada')    


@blueprint.get('/layers')
def get_layers():
    """
    Rota GET para acessar todas as Camadas
    """
    motor = Motor()
    layers = motor.get_all_layers().to_dict(orient='records')
    try:          
        return Response(
            json.dumps(layers, ensure_ascii=False),
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

@blueprint.get('/layer/<int:layer_id>')
def get_layer_by_id(path: Path):
    """
    Rota GET para acessar as Camadas por id
    """
    motor = Motor()
    layer = motor.get_layers_by_id([path.layer_id]).to_dict(orient='records')
    return Response(
        json.dumps(layer, ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/layer/<int:layer_id>')
def delete_layer_by_id(path: Path):
    """
    Rota DELETE das Camadas por id
    """
    motor = Motor()
    layer = motor.get_layers_by_id([path.layer_id])
    if len(layer):
        data_update = [{'id': path.layer_id, 'status': 'inactive'}]
        motor.update_item('layers', data_update)
        return Response(
            json.dumps(
                {
                    'msg': 'Camada deletada com sucesso',
                    'deleted': layer.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe camada para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.put('/layer/<int:layer_id>')
def update_layer(path: Path, query: LayerBody):
    """
    Rota PUT para atualização de Camada por id
    """
    motor = Motor()
    previous_layer = motor.get_layers_by_id([path.layer_id])
    if len(previous_layer):
        data_update = {key: value for key, value in query.model_dump().items() if value is not None}
        data_update['id'] = path.layer_id
        motor.update_item('layers', [data_update])
        updated_layer = motor.get_layers_by_id([path.layer_id])
        return Response(
            json.dumps(
                {
                    'msg': 'Camada atualizada com sucesso',
                    'previous': previous_layer.to_dict(orient='records'),
                    'updated': updated_layer.to_dict(orient='records')
                },
                ensure_ascii=False
            ),
            mimetype="application/json",
            status=200,
        )
    return Response(
        json.dumps(
            {'msg': 'Não existe camada para os parâmetros informados'},
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=422,
    )

@blueprint.post('/layer')
def add_layer(body: LayerBody):
    """
    Rota POST para adicionar Nova Camada
    """
    motor = Motor()
    data_save = body.model_dump().copy()
    data_save['id'] = None
    motor.add_item('layers', [data_save])
    return Response(
        json.dumps(
            {"message": "Camada inserida com sucesso",
            "layer": body.model_dump()
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )
