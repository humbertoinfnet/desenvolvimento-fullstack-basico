from abc import abstractclassmethod
from src.external_interfaces.database.controllers.templates import MotorTemplate


class Motorinterface(MotorTemplate):

    @abstractclassmethod
    def get_all_layers(self):
        raise NotImplementedError('Método não implementado')