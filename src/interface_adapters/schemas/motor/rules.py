from typing import Optional
from pydantic import BaseModel, Field, RootModel


class PathRule(BaseModel):
    rule_id: int = Field(..., description='Id da regra')


class BodyRule(BaseModel):
    name: Optional[str] = Field(None, description='Nome da regra')
    code: Optional[str] = Field(None, description='Código da regra')
    rule: Optional[str] = Field(None, description='Lógica da regra')
    description: Optional[str] = Field(None, description='Descrição da regra')


class ResponseRule(BaseModel):
    rule_id: int = Field(None, description='Id da regra')
    name: str = Field(None, description='Nome da regra')
    code: str = Field(None, description='Código da regra')
    description: str = Field(None, description='Descrição da regra')
    identify: str = Field(None, description='Identificacao do elemento')
    rule: str = Field(None, description='Lógica da regra')


class ResponseSuccessRule(RootModel):
    root: list[ResponseRule]


class ResponseSuccessRuleDelete(BaseModel):
    message: str = Field("success_delete_rule", description="Mensagem do response")
    deleted: list[ResponseRule]


class ResponseSuccessRuleUpdate(BaseModel):
    message: str = Field("success_update_rule", description="Mensagem do response")
    previous: list[ResponseRule]
    updated: list[ResponseRule]


class ResponseSuccessRuleAdd(BaseModel):
    message: str = Field("success_add_rule", description="Mensagem do response")
    create: list[ResponseRule]
