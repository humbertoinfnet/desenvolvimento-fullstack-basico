# project/infra/database/models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.entities.cadastral_user import User as UserDomainEntity

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    def to_domain_entity(self):
        return UserDomainEntity(
            user_id=self.id,
            username=self.username,
            email=self.email
        )