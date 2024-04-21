import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import URL
import warnings
import json
from flask import current_app

warnings.filterwarnings("ignore")


class DBConnection:
    """Classe responsável por controlar a conexão com o banco de dados utilizando Sqlalchemy
    """
    def __init__(self, database_name) -> None:
        current_app.logger.info('[DBConnection] - executa método construtor da classe')
        self.params = self.get_params(database_name)
        self.session = self.__get_session()

    def __enter__(self):
        return self

    def __get_session(self) -> Session:
        """Método responsável por criar a conexão com o banco
        """

        current_app.logger.info('[DBConnection] - executa método get_session')
        url = self.create_connection_url()
        engine = create_engine(url, pool_recycle=3600)
        session = sessionmaker(bind=engine)
        return session()

    def get_params(self, database_name: str) -> dict:
        """Método responsável por buscar os parâmetros de conexão
        """

        current_app.logger.info('[DBConnection] - executa método get_params')
        with open(f'src/external_interfaces/database/config/connections.json') as arq:
            params = json.load(arq)
        return params.get(database_name)

    def create_connection_url(self) -> str:
        """Método responsável por criar a url de conexão
        """

        current_app.logger.info('[DBConnection] - executa método create_connection_url')
        return URL.create(
            drivername=self.params.get('dialect'),
            username=self.params.get('username'),
            password=self.params.get('password'),
            host=self.params.get('host'),
            port=self.params.get('port'),
            database=self.params.get('database')
        )

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if not exc_traceback:
            if isinstance(self.session, Session):
                self.session.rollback()
        self.session.close()
