"""Defines the REST functionality and returns a response object"""

import json
from flask import redirect
from flask_openapi3 import Tag, APIBlueprint


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
blueprint = APIBlueprint('home', __name__, abp_tags=[home_tag])


@blueprint.get('/', doc_ui=True)
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')
