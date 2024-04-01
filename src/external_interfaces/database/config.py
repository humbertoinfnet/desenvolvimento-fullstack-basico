
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurações do banco de dados (substitua pelos seus próprios valores)
DATABASE_URL = "sqlite:///example.db"

# Criar uma instância de engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar uma instância de Session do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
