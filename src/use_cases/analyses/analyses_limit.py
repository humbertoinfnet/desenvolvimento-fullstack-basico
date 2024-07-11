import pandas as pd
import numpy as np
from collections import OrderedDict
from dataclasses import dataclass
from src.interface_adapters.database.controllers.analyses import Motorinterface


@dataclass
class AnalysesLimit:
    document: str
    data: dict

    def __post_init__(self):
        self.response_limit = dict()

    def execute(self):
        self.handle_data()
        self.application_rule()
        return self.response_limit

    def handle_data(self):
        data = {}
        for key in self.data.get('data').keys():
            data.update(self.data.get('data').get(key))
        self.data = data.copy()
        del data

    def application_rule(self):
        limit_max = round((self.data.get('faturamento', 0) * 0.01), 2)
        classification, perc_limit = self.matrix(self.data.get('score_risco', 0))
        limit_calc = round(limit_max * perc_limit, 2)
        self.response_limit = {
            'limite_max': limit_max,
            'limite_calc': limit_calc,
            'classificacao': classification,
        }

    def matrix(self, score: int):
        conditions = [
            (score >= 0 and score < 100),
            (score >= 100 and score < 200),
            (score >= 200 and score < 400),
            (score >= 400 and score < 600),
            (score >= 600 and score < 800),
            (score >= 800 and score < 1000)
        ]
        classification_matrix = OrderedDict([('E', 0),('D', 0),('C', 0.4),('B', 0.6),('A', 0.8),('AA', 1)])
        x = np.arange(6)
        classification = np.select(conditions, classification_matrix.keys(), default='erro')
        perc_limit = np.select(conditions, classification_matrix.values(), default=0)
        return classification.item(), perc_limit.item()
