"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurações do banco de dados (substitua pelos seus próprios valores)
DATABASE_URL = "sqlite:///example.db"

# Criar uma instância de engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar uma instância de Session do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""


from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from src.external_interfaces.database.model.base import Base
from src.external_interfaces.database.model.motor import *

def init_database():
    db_path = "files/database"
    # Verifica se o diretorio não existe
    if not os.path.exists(db_path):
        # então cria o diretorio
        os.makedirs(db_path)

    # url de acesso ao banco (essa é uma url de acesso ao sqlite local)
    db_url = 'sqlite:///%s/db.sqlite3' % db_path

    # cria a engine de conexão com o banco
    engine = create_engine(db_url, echo=False)

    # # Instancia um criador de seção com o banco
    # Session = sessionmaker(bind=engine)

    # cria o banco se ele não existir 
    if not database_exists(engine.url):
        create_database(engine.url) 

    # cria as tabelas do banco, caso não existam
    Base.metadata.create_all(engine)