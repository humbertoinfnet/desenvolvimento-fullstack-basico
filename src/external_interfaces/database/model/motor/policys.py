from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from src.external_interfaces.database.model.base import Base


class Policys(Base):
    """
    Classe do sqlalchemy que mapeia a tabela policys em banco
    """

    __tablename__ = "policys"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    identify = Column(String, nullable=True, default='policy')
    description = Column(String, nullable=False)
    status = Column(Enum('active', 'inactive'), default='active', nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
