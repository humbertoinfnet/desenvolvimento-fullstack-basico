from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from src.external_interfaces.database.model.base import Base


class Layers(Base):
    """
    Classe do sqlalchemy que mapeia a tabela layers em banco
    """
    
    __tablename__ = "layers"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    identify = Column(String, nullable=True, default='layer')
    description = Column(String, nullable=False)
    status = Column(Enum('active', 'inactive'), default='active', nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=True)
