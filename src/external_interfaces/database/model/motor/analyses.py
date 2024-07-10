from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON
from src.external_interfaces.database.model.base import Base


class Analyses(Base):
    """
    Classe do sqlalchemy que mapeia a tabela rules em banco
    """

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    document = Column(String, index=True, nullable=False, unique=True)
    type_policy = Column(String, index=True, nullable=False)
    limit = Column(String, nullable=True)
    decision = Column(String, nullable=True)
    analyses_detail_id = Column(Integer)
    data =  Column(JSON(none_as_null=True), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
