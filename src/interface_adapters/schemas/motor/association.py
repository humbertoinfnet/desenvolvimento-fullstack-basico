from typing import Literal, List
from pydantic import BaseModel, Field, RootModel, ConfigDict


class BodyAssociationLayersPolicys(BaseModel):
    policy_id: int = Field(None, gt=0, description='Id da política')
    layer_id: int = Field(None, gt=0, description='Id da camada')


class BodyAssociationRulesLayers(BaseModel):
    rule_id: int = Field(None, gt=0, description='Id da regra')
    layer_id: int = Field(None, gt=0, description='Id da camada')
    action: Literal['refuse', 'pendency'] = Field(description="Ação que a regra deverá fazer")


class QueryUpdateAssociationRulesLayers(BaseModel):
    action: Literal['refuse', 'pendency'] = Field(description="Ação que a regra deverá fazer")


class PriorityLayersPolicys(BaseModel):
    association_id: int = Field(None, gt=0, description='id referente a associação')
    priority: int = Field(None, ge=0, description='Prioridade da camada na política')


class BodyPrioritys(BaseModel):
    prioritys: list[PriorityLayersPolicys] = Field(None, description='Json com a estrutura de prioridade das camadas')

class PathAssociation(BaseModel):
    association_id: int = Field(None, gt=0, description='Id da associação')


class PathLayersPolicys(BaseModel):
    index_id: int = Field(None, gt=0, description='Número do id')
    type_id: Literal['association_id', 'policy_id', 'layer_id'] = Field(description="Tipo de id para a busca")


class PathRulesLayers(BaseModel):
    index_id: int = Field(None, gt=0, description='Número do id')
    type_id: Literal['association_id', 'layer_id', 'rule_id'] = Field(description="Tipo de id para a busca")


class ResponseAssociationRulesLayers(BaseModel):
    association_id: int = Field(1, gt=0, description='Id da associação')
    name_layer: str = Field(None, description='Nome da camada')
    name_rule: str = Field(None, description='Nome da regra')
    layer_id: int = Field(1, gt=0, description='Id da camada')
    rule_id: int = Field(1, gt=0, description='Id da regra')
    action: str = Field(None, description='Ação atrelada a regra na camada')
    identify: str = Field(None, description='Identificacao do elemento')


class ResponseAssociationLayersPolicys(BaseModel):
    association_id: int = Field(1, gt=0, description='Id da associação')
    name_policy: str = Field(None, description='Nome da política')
    name_layer: str = Field(None, description='Nome da camada')
    layer_id: int = Field(1, gt=0, description='Id da camada')
    policy_id: int = Field(1, gt=0, description='Id da política')
    priority: str = Field(None, description='Prioridade da camada na política')
    identify: str = Field(None, description='Identificacao do elemento')


class ResponseSuccessAssociationRulesLayers(RootModel):
    root: list[ResponseAssociationRulesLayers]


class ResponseSuccessAssociationRulesLayersDelete(BaseModel):
    message: str = Field("success_delete_association_rules_layers", description="Mensagem do response")
    deleted: list[ResponseAssociationRulesLayers]


class ResponseSuccessAssociationRulesLayersUpdate(BaseModel):
    message: str = Field("success_update_association_rules_layers", description="Mensagem do response")
    previous: list[ResponseAssociationRulesLayers]
    updated: list[ResponseAssociationRulesLayers]


class ResponseSuccessAssociationRulesLayersAdd(BaseModel):
    message: str = Field("success_add_association_rules_layers", description="Mensagem do response")
    create: list[ResponseAssociationRulesLayers]


class ResponseSuccessAssociationLayersPolicys(RootModel):
    root: list[ResponseAssociationLayersPolicys]


class ResponseSuccessAssociationLayersPolicysDelete(BaseModel):
    message: str = Field("success_delete_association_policy_layers", description="Mensagem do response")
    deleted: list[ResponseAssociationLayersPolicys]


class ResponseSuccessAssociationLayersPolicysUpdate(BaseModel):
    message: str = Field("success_update_association_policy_layers", description="Mensagem do response")
    prioritys: list[ResponseAssociationLayersPolicys]


class ResponseSuccessAssociationLayersPolicysAdd(BaseModel):
    message: str = Field("success_add_association_policy_layers", description="Mensagem do response")
    create: list[ResponseAssociationLayersPolicys]
