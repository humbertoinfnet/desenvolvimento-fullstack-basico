from dataclasses import dataclass

from typing import Optional, Literal
from src.interface_adapters.database.controllers.motor import Motorinterface
from .update_association import UpdateAssociation
from .rules import Rule
from .layers import Layers
from .policys import Policys
from .association import Association


@dataclass
class MotorConfig:
    motor: Motorinterface
    update_association: UpdateAssociation

    def __post_init__(self):
        self.rule = Rule(self.motor, self.update_association)
        self.layers = Layers(self.motor, self.update_association)
        self.policys = Policys(self.motor, self.update_association)
        self.association = Association(self.motor)
