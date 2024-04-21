from typing import Optional
from pydantic import BaseModel, Field, RootModel


class PathPolicy(BaseModel):
    policy_id: int = Field(..., description='Id da política')


class BodyPolicy(BaseModel):
    name: Optional[str] = Field(None, description='Nome da política')
    description: Optional[str] = Field(None, description='Descrição da política')


class ResponsePolicy(BaseModel):
    policy_id: int = Field(None, description='Id da política')
    name: str = Field(None, description='Nome da política')
    description: str = Field(None, description='Descrição da política')
    identify: str = Field(None, description='Identificacao do elemento')


class ResponseSuccessPolicy(RootModel):
    root: list[ResponsePolicy] = Field(description="Array dos objetos")


class ResponseSuccessPolicyDelete(BaseModel):
    message: str = Field("success_delete_policy", description="Mensagem do response")
    deleted: list[ResponsePolicy]


class ResponseSuccessPolicyUpdate(BaseModel):
    message: str = Field("success_update_policy", description="Mensagem do response")
    previous: list[ResponsePolicy]
    updated: list[ResponsePolicy]


class ResponseSuccessPolicyAdd(BaseModel):
    message: str = Field("success_add_policy", description="Mensagem do response")
    create: list[ResponsePolicy]
