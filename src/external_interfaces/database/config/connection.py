import getpass
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import URL
import warnings
import json
warnings.filterwarnings("ignore")


class DBConnection:
    def __init__(self, database_name) -> None:
        self.params = self.get_params(database_name)
        self.session = self.__get_session()

    def __enter__(self):
        return self

    def __get_session(self):
        url = self.create_connection_url()
        engine = create_engine(url, pool_recycle=3600)
        session = sessionmaker(bind=engine)
        return session()

    def get_params(self, database_name):
        with open(f'src/external_interfaces/database/config/connections.json') as arq:
            params = json.load(arq)
        return params.get(database_name)

    def create_connection_url(self):
        return URL.create(
            drivername=self.params.get('dialect'),
            username=self.params.get('username'),
            password=self.params.get('password'),
            host=self.params.get('host'),
            port=self.params.get('port'),
            database=self.params.get('database')
        )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not exc_traceback:
            if isinstance(self.session, Session):
                self.session.rollback()
        self.session.close()
