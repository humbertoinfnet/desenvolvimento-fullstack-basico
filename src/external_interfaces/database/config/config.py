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


from src.external_interfaces.database.model.base import Base

from src.external_interfaces.database.controllers.motor import Motor


def init_database():
    db_path = "files/database"

    if not os.path.exists(db_path):

        os.makedirs(db_path)


    db_url = 'sqlite:///%s/db.sqlite3' % db_path

    engine = create_engine(db_url, echo=False)

 
    if not database_exists(engine.url):
        create_database(engine.url) 


    Base.metadata.create_all(engine)

def exemple_policys():
    return [
        {
            "name": "PoliticaCartaoPJ",
            "description": "Política para produto cartão referente ao tipo de documento CNPJ"
        },
        {
            "name": "PoliticaCartaoPF",
            "description": "Política para produto cartão referente ao tipo de documento PF"
        },
        {
            "name": "PoliticaAntecipacaoCedente",
            "description": "Política para produto antecipacao vinculado ao Cedente"
        }
    ]

def exemple_layers():
    return [
        {
            "name": "camada_sem_custo",
            "description": "Camada com as regras sem custo de consulta"
        },
        {
            "name": "camada_baixo_custo",
            "description": "Camada com as regras com baixo custo de consulta"
        },
        {
            "name": "camada_medio_custo",
            "description": "Camada com as regras com custo médio de consulta"
        }
    ]

def exemple_rules():
    return [
        {
            "name": "REP001-TempoConta",
            "code": "REP001",
            "rule": "TempoConta > 30",
            "description": "Regra para tempo de conta"
        },
        {
            "name": "REP002-ScoreSerasa",
            "code": "REP002",
            "rule": "ScoreSerasa > 800",
            "description": "Regra para score Serasa"
        },
        {
            "name": "REP003-SituacaoDocumento",
            "code": "REP003",
            "rule": "SituacaoDocumento == 'Regular'",
            "description": "Situação do documento na receita"
        }
    ]

def exemple_rules_to_layers():
    return [
        {
            "layer_id": 1,
            "rule_id": 1,
            "action": "refuse"
        },
        {
            "layer_id": 2,
            "rule_id": 3,
            "action": "pendency"
        },
        {
            "layer_id": 3,
            "rule_id": 2,
            "action": "refuse"
        }
    ]

def exemple_layers_to_policys():
    return [
        {
            "policy_id":1,
            "layer_id": 2,
            "priority": 0
        },
        {
            "policy_id": 2,
            "layer_id": 2,
            "priority": 0
        },
        {
            "policy_id": 3,
            "layer_id": 3,
            "priority": 0
        }
    ]

def insert_elements():
    motor = Motor()
    data_insert = {
        'policys': exemple_policys,
        'layers': exemple_layers,
        'rules': exemple_rules,
        'rules_to_layers': exemple_rules_to_layers,
        'layers_to_policys': exemple_layers_to_policys,
    }
    for key, value in data_insert.items():  
        try:
            motor.add_item(key, value())
        except:
            pass