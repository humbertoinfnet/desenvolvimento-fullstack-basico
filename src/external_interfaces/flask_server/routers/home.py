"""Defines the REST functionality and returns a response object"""

import json
from flask import request, Response, redirect
from flask_openapi3 import Tag, APIBlueprint


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
blueprint = APIBlueprint('home', __name__, abp_tags=[home_tag])


@blueprint.get('/', doc_ui=True)
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# @blueprint.route('/', methods=["GET"])
# def home():
#     """
#     Defines a GET route for the arxiv API.
#     Make the request object API ready.
#     Transform the response into JSON format

#     Returns:
#         object (JSON): A response object for further querying
#     """

#     return Response(
#         json.dumps({'msg': 'teste', 'status': 200}),
#         mimetype="application/json",
#         status=200,
#     )
    # qrystr_params = {"filters": {}}

    # for arg, values in request.args.items():
    #     if arg.startswith("filter_"):
    #         qrystr_params["filters"][arg.replace("filter_", "")] = values

    # request_object = req.ArxivDocumentListRequestObject.from_dict(qrystr_params)

    # repo = ar.ArxivRepo()
    # use_case = uc.ProcessArxivDocuments(repo)

    # response = use_case.execute(request_object)

    # return Response(
    #     json.dumps(response.value, cls=ser.ArxivDocEncoder),
    #     mimetype="application/json",
    #     status=STATUS_CODES[response.type],
    # )
