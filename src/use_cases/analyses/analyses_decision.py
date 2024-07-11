import pandas as pd
from dataclasses import dataclass
from src.interface_adapters.database.controllers.analyses import Motorinterface


@dataclass
class AnalysesDecision:
    document: str
    type_policy: str
    motor: Motorinterface
    data: dict

    def __post_init__(self):
        self.policy_rule = pd.DataFrame()
        self.response_decision = dict()

    def execute(self):
        self.get_policy_rule()
        self.handle_data()
        self.application_rule()
        return self.response_decision 
    
    def get_policy_rule(self):
        self.policy_rule = self.motor.get_policy_rule(self.type_policy)

    def handle_data(self):
        data = {}
        for key in self.data.get('data').keys():
            data.update(self.data.get('data').get(key))
        self.data = data.copy()
        del data

    def application_rule(self):
        response = []
        groups_layers = self.policy_rule.groupby('layer_name')

        final_result = 'APROVADO'
        for group, data_group in groups_layers:
            rules = data_group[['rule_name', 'code', 'rule', 'description', 'action']].to_dict('records')
            decision_layer = self.decision(rules, group)
            response.append(decision_layer)
            final_result = self.handle_final_result(decision_layer.get('decisao'), final_result)

        self.response_decision = {
            'decisao': final_result,
            'decisao_detalhada': response
        }

    def decision(self, rules, layer):
        decisao_rule_rep = []
        decisao_rule_pen = []
        errors = []
        for rule in rules:
            try:
                pd.eval(rule.get('rule'), local_dict=self.data)
                result = eval(rule.get('rule'), {}, self.data)
                if result:
                    variavel = set(var for var in self.data.keys() if var in rule.get('rule')).pop()
                    rule['variavel_regra'] = {variavel: self.data.get(variavel)}
                    if rule.get('action') == 'refuse':
                        decisao_rule_rep.append(rule)
                    else:
                        decisao_rule_pen.append(rule)
            except Exception as err:
                decisao_rule_error = rule.copy()
                decisao_rule_error['motivo_erro'] = str(err)
                errors.append(decisao_rule_error)
        layer_result = 'PENDENTE' if len(decisao_rule_pen) > 0 else 'APROVADO'
        layer_result = 'REPROVADO' if len(decisao_rule_rep) > 0 else layer_result
        layer_result = 'ERRO' if len(errors) > 0 else layer_result
        
        decisao = {
            'processo': layer,
            'decisao': layer_result,
            'codigos_rep': decisao_rule_rep if decisao_rule_rep else None,
            'codigos_pen': decisao_rule_pen if decisao_rule_pen else None,
        }
        if errors:
            decisao['erros'] = errors
        return decisao
    
    def handle_final_result(self, layer_result, final_result):
        priority = ['ERRO', 'REPROVADO', 'PENDENTE', 'APROVADO']
        return priority[min([priority.index(layer_result), priority.index(final_result)])]
