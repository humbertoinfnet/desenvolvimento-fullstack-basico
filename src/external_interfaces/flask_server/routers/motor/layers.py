import json

from typing import Optional
from pydantic import BaseModel, Field

from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint



from src.interface_adapters.request_arxiv.rest_adapters import request_object as res


tag = Tag(name="Camadas", description="Camadas")
blueprint = APIBlueprint('layers', __name__, abp_tags=[tag], doc_ui=True)


class Query(BaseModel):
    origin_id: int = Field(..., description='origem id')
    destino_id: int = Field(..., description='destino id')

class BookQuery(BaseModel):
    type: str

class Path(BaseModel):
    layer_id: int = Field(..., description='layer id')

class layerBody(BaseModel):
    name: Optional[str] = Field(None, description='Nome da regra')
    type: Optional[str] = Field(None, description='Lógica da regra')
    description: Optional[str] = Field(None, description='Descrição da regra')


layers = [
    {
        'id': 0,
        'name': 'layer_0',
        'type': 'layer',
        'description': 'Camada dos filtros duros para informações internas não pagas'
    },
    {
        'id': 1,
        'name': 'layer_1',
        'type': 'layer',
        'description': 'Camada de filtro duro para informações pagas até 1 real'
    },
    {
        'id': 2,
        'name': 'layer_2',
        'type': 'layer',
        'description': 'Camada de filtro duro para informações pagas de 1 real até 2 reais'
    }
    
]

@blueprint.get('/layers')
def get_layers():
    """
    Rota GET para acessar as Camadas e layers cadastradas
    """

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
    Rota GET para acessar as Camadas cadastradas por id
    """
    return Response(
        json.dumps(layers[path.layer_id], ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.delete('/layer/<int:layer_id>')
def delete_layer_by_id(path: Path):
    """
    Rota DELETE para deletar as Camadas cadastradas por id
    """
    return Response(
        json.dumps(
            {
                'msg': 'Camada deletada com sucesso',
                'layer': layers[path.layer_id]
            },
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )

@blueprint.put('/layers/<int:layer_id>')
def update_layer(path: Path, query: layerBody):
    """
    Rota para atualização de Camada
    """
    for key, value in query.model_dump().items():
        if value is not None:
            layers[path.layer_id][key] = value
    return Response(
        json.dumps(layers[path.layer_id], ensure_ascii=False),
        mimetype="application/json",
        status=200,
    )

@blueprint.post('/layers')
def add_layer(body: layerBody):
    """
    Rota para adicionar Nova Camada
    """
    layers.append(body.model_dump())
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

@blueprint.post('/associate-layers-to-polices')
def associate_layers_to_polices(query: Query):
    """
    Rota para associar camada com politica
    """
    
    return Response(
        json.dumps(
            {"message": "Camada associada com sucesso",
            "associate": f"{layers[query.origin_id]['name']} com Política {query.destino_id}"
            }, 
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )


@blueprint.post('/associate-rules-to-layers')
def associate_rules_to_layers(query: Query):
    """
    Rota para associar regra com camada
    """
    
    return Response(
        json.dumps(
            {"message": "Camada associada com sucesso",
            "associate": f"Regra {query.origin_id} com Camada {layers[query.destino_id]['name']}"
            },  
            ensure_ascii=False
        ),
        mimetype="application/json",
        status=200,
    )