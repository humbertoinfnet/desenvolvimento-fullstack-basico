from typing import Optional
from pydantic import BaseModel, Field, RootModel


class PathAnalyses(BaseModel):
    document: str = Field(None, description='Documento para analise')
    type_policy: str = Field(None, description='Nome da política para execução da analise')
