import json
from flask import request, Response
from flask_openapi3 import Tag, APIBlueprint

from src.interface_adapters.request_arxiv.rest_adapters import request_object as res


arxiv_tag = Tag(name="Politicas", description="Politicas")
blueprint = APIBlueprint('politicas', __name__, abp_tags=[arxiv_tag])


@blueprint.get('/cadastro-politica', doc_ui=True)
def cadastro():
    """
    Defines a GET route for the arxiv API.
    Make the request object API ready.
    Transform the response into JSON format

    Returns:
        object (JSON): A response object for further querying
    """

    return Response(
        json.dumps({'msg': 'teste', 'status': 200}),
        mimetype="application/json",
        status=200,
    )
