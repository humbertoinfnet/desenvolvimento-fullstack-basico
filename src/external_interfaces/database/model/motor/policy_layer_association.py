from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, UniqueConstraint

from src.external_interfaces.database.model.base import Base


class PolicyLayerAssociation(Base):
    __tablename__ = 'policy_layer_association'

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    policy_id = Column(Integer, ForeignKey('policys.id'))
    layer_id = Column(Integer, ForeignKey('layers.id'))
    priority = Column(Integer, nullable=False)
    name_layer = Column(String, nullable=False)
    name_policy = Column(String, nullable=False)
    identify = Column(String, nullable=True, default='policy_layer_association')
    status = Column(Enum('active', 'inactive'), default='active', nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


    __table_args__ = (
        UniqueConstraint('policy_id', 'layer_id'),
        UniqueConstraint('policy_id', 'priority'),
    )
