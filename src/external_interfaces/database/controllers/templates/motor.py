from abc import ABC
from src.external_interfaces.database.config import DBConnection


class MotorTemplate(ABC):
    """
    Template method para o banco motor.
    """

    __name__ = "Motor"

    def __init__(self) -> None:
        self.dbconn = DBConnection
        self.database = "motor"
        self.dialect = "sqlite"
