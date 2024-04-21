from dataclasses import dataclass

from src.interface_adapters.database.controllers.motor import Motorinterface
from .update_association import UpdateAssociation
from .rules import Rules
from .layers import Layers
from .policys import Policys
from .association import Association


@dataclass
class MotorConfig:
    """
    Classe responsável por fazer por centralizar as requisições das lógicas
    """

    motor: Motorinterface
    update_association: UpdateAssociation

    def __post_init__(self):
        self.rules = Rules(self.motor, self.update_association)
        self.layers = Layers(self.motor, self.update_association)
        self.policys = Policys(self.motor, self.update_association)
        self.association = Association(self.motor)
