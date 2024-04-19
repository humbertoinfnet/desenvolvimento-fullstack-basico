# def update_association(path, query, type_association):
#     motor = Motor()
#     if type_association == 'layers_to_policys':
#         association = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
#     else:
#         association = motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
#     if len(association):
#         data_update = {key: value for key, value in query.model_dump().items() if value is not None}
#         data_update['id'] = path.association_id
#         motor.update_item(type_association, [data_update])
#         association_update = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
#         return Response(
#             json.dumps(
#                 {
#                     'msg': 'Associação atualizada com sucesso',
#                     'previous': association.to_dict(orient='records'),
#                     'updated': association_update.to_dict(orient='records')
#                 },
#                 ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=200,
#         )
#     return Response(
#         json.dumps(
#             {'msg': 'Não existe associação para os parâmetros informados'},
#             ensure_ascii=False
#         ),
#         mimetype="application/json",
#         status=422,
#     )

# def delete_association(path: Path, type_association):
#     """
#     Rota DELETE para deletar as Associações por id
#     """
#     motor = Motor()
#     if type_association == 'layers_to_policys':
#         association = motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
#     else:
#         association = motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
#     if len(association):
#         data_update = association.copy()
#         data_update['status'] = 'inactive'
#         data_update.rename(columns={'association_id': 'id'}, inplace=True)
#         motor.update_item(type_association, data_update.to_dict(orient='records'))
#         return Response(
#             json.dumps(
#                 {
#                     'msg': 'Associação deletada com sucesso',
#                     'deleted': association.to_dict(orient='records')
#                 },
#                 ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=200,
#         )
#     return Response(
#         json.dumps(
#             {'msg': 'Não existe associação para os parâmetros informados'},
#             ensure_ascii=False
#         ),
#         mimetype="application/json",
#         status=422,
#     )








# @blueprint.get('/associate-layers-to-policys')
# def get_all_layers_to_policys():
#     """
#     Rota GET para acessar todas as Associações Camadas com Política
#     """
#     motor = Motor()
#     association = motor.get_all_association_layer_to_police().to_dict(orient='records')
#     try:          
#         return Response(
#             json.dumps(association, ensure_ascii=False),
#             mimetype="application/json",
#             status=200,
#         )
        
#     except:
#         return Response(
#             json.dumps(
#                 {
#                     'msg': 'erro',
#                 }
#             ),
#             mimetype="application/json",
#             status=500,
#         )

# @blueprint.get('/associate-layers-to-policys/<int:index_id><string:type_id>')
# def get_layers_to_policys_by_id(path: PathLayersPolicys):
#     """
#     Rota GET para acessar a Associação Camadas com Política por id
#     """
#     motor = Motor()
#     association = (
#         motor
#         .get_association_layer_to_police_by_id(path.type_id, [path.index_id])
#         .sort_values('priority')
#         .to_dict(orient='records')
#     )
#     return Response(
#         json.dumps(association, ensure_ascii=False),
#         mimetype="application/json",
#         status=200,
#     )

# @blueprint.delete('/associate-layers-to-policys/<int:association_id>')
# def delete_layers_to_policys(path: Path):
#     """
#     Rota DELETE da Associação Camadas com Política
#     """
#     return delete_association(path, 'layers_to_policys')

# @blueprint.post('/associate-layers-to-policys')
# def associate_layers_to_policys(body: QueryAssociationLayersPolicys):
#     """
#     Rota POST para adicionar nova Associação Camadas com Política
#     """
#     motor = Motor()
#     policy = motor.get_policys_by_id([body.policy_id])
#     layer = motor.get_layers_by_id([body.layer_id])
#     other_layers_association = (
#         motor
#         .get_association_layer_to_police_by_id('policy_id', [body.policy_id])
#     )
#     if len(policy) and len(layer):
        
#         layers_to_policys = motor.get_all_association_layer_to_police(status='inactive')
#         layers_to_policys_update = layers_to_policys.query(f'layer_id == {body.layer_id} and policy_id == {body.policy_id}')
#         if len(layers_to_policys_update):
#             layers_to_policys_update["priority"] = len(other_layers_association)
#             layers_to_policys_update['status'] = 'active'
#             layers_to_policys_update.rename(columns={'association_id':'id'}, inplace=True)
#             motor.update_item('layers_to_policys', layers_to_policys_update.to_dict(orient='records'))
#             id_save = layers_to_policys_update['id'].to_list()
#         else:
            
#             data_save = {
#                 'id': None,
#                 'policy_id': body.policy_id,
#                 'layer_id': body.layer_id,
#                 'priority': len(other_layers_association)
#             }
#             id_save = motor.add_item('layers_to_policys', [data_save])
#         association_create = (
#             motor
#             .get_association_layer_to_police_by_id('association_id', id_save)
#             .to_dict(orient='records')
#         )
#         return Response(
#             json.dumps(
#                 {
#                     "message": "Associação realizada com sucesso",
#                     "association": f"Política: {policy.loc[0,'name']} com Camada: {layer.loc[0,'name']}",
#                     "create": association_create
#                 }, 
#                 ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=200,
#         )
#     elif len(policy):
#         msg = 'Não existe camada para os parâmetros informados'
#     else:
#         msg = 'Não existe política para os parâmetros informados'
#     return Response(
#         json.dumps(
#             {'msg': msg},
#             ensure_ascii=False
#         ),
#         mimetype="application/json",
#         status=422,
#     )

# @blueprint.post('/associate-layers-to-policys/alter-priority')
# def alter_priority_layers_to_policys(body: BodyPrioritys):
#     """
#     Rota POST responsável por alterar as prioridades das camadas na Associação Camadas com Política
#     """
#     itens = []
#     association_id = []
    
    
#     for item in body.prioritys:
#         itens.append(item.model_dump())
#         association_id.append(item.association_id)
#     motor = Motor()
#     association = motor.get_all_association_layer_to_police()
#     if association.query('association_id in @association_id')['policy_id'].nunique() > 1:
#         return Response(
#             json.dumps(
#                 {
#                     'msg': 'a ordenacao deve ser feita apenas uma politica por vez'
#                 }
#                 , ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=500,
#         )
#     policy_id = association.query('association_id in @association_id')['policy_id'].unique()
#     itens_not_informed = (
#         association
#         .query('policy_id in @policy_id')
#         .query('association_id not in @association_id')['association_id']
#         .to_list()
#     )
#     if itens_not_informed:
#         return Response(
#             json.dumps(
#                 {
#                     'association_id_not_informed': itens_not_informed
#                 }
#                 , ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=200,
#         )

#     prioritys = pd.DataFrame(itens)
#     prioritys = prioritys.sort_values(['priority', 'association_id']).reset_index(drop=True)
#     prioritys['priority'] = prioritys.index
#     motor.update_item('layers_to_policys', prioritys.rename(columns={'association_id': 'id'}).to_dict(orient='records'))
#     return Response(
#         json.dumps(
#             {
#                 "message": "Prioridades atualizadas com sucesso",
#                 "prioritys": prioritys.to_dict(orient='records')
#             }, 
#             ensure_ascii=False
#         ),
#         mimetype="application/json",
#         status=200,
#     )




# @blueprint.get('/associate-rules-to-layers')
# def get_rules_to_layers():
#     """
#     Rota GET para acessar todas as Associações Regras com Camada
#     """
#     motor = Motor()
#     association = motor.get_all_association_rule_to_layer().to_dict(orient='records')
#     try:          
#         return Response(
#             json.dumps(association, ensure_ascii=False),
#             mimetype="application/json",
#             status=200,
#         )
        
#     except:
#         return Response(
#             json.dumps(
#                 {
#                     'msg': 'erro',
#                 }
#             ),
#             mimetype="application/json",
#             status=500,
#         )

# @blueprint.get('/associate-rules-to-layers/<int:index_id><string:type_id>')
# def get_rules_to_layers_by_id(path: PathRulesLayers):
#     """
#     Rota GET para acessar a Associação Regras com Camada por id
#     """
#     motor = Motor()
#     association = (
#         motor
#         .get_association_rule_to_layer_by_id(path.type_id, [path.index_id])
#         .to_dict(orient='records')
#     )
#     return Response(
#         json.dumps(association, ensure_ascii=False),
#         mimetype="application/json",
#         status=200,
#     )

# @blueprint.delete('/associate-rules-to-layers/<int:association_id>')
# def delete_rules_to_layers(path: Path):
#     """
#     Rota DELETE da Associação Regras com Camada
#     """
#     return delete_association(path, 'rules_to_layers')

# @blueprint.put('/associate-rules-to-layers/<int:association_id>')
# def update_rules_to_layers(path: Path, query: UpdateAssociationRulesLayers):
#     """
#     Rota PUT para alteração da Ação da regra na Associação Regras com Camada
#     """
#     return update_association(path, query, 'rules_to_layers')

# @blueprint.post('/associate-rules-to-layers')
# def associate_rules_to_layers(body: QueryAssociationRulesLayers):
#     """
#     Rota POST para adicionar nova Associação Regras com Camada
#     """
#     motor = Motor()
#     layer = motor.get_layers_by_id([body.layer_id])
#     rule = motor.get_rules_by_id([body.rule_id])
#     if len(rule) and len(layer):
#         rule_to_layer = motor.get_all_association_rule_to_layer(status='inactive')
#         rule_to_layer_update = rule_to_layer.query(f'layer_id == {body.layer_id} and rule_id == {body.rule_id}')
#         if len(rule_to_layer_update): 
#             rule_to_layer_update["action"] = body.action
#             rule_to_layer_update['status'] = 'active'
#             rule_to_layer_update.rename(columns={'association_id': 'id'}, inplace=True)
#             motor.update_item('rules_to_layers', rule_to_layer_update.to_dict(orient='records'))
#             id_save = rule_to_layer_update['id'].to_list()
#         else:
            
#             data_save = {
#                 'id': None,
#                 "layer_id": body.layer_id,
#                 "rule_id": body.rule_id,
#                 "action": body.action
#             }
#             id_save = motor.add_item('rules_to_layers', [data_save])
#         association_create = (
#             motor
#             .get_association_rule_to_layer_by_id('association_id', id_save)
#             .to_dict(orient='records')
#         )
#         return Response(
#             json.dumps(
#                 {
#                     "message": "Associação realizada com sucesso",
#                     "association": f"Camada: {layer.loc[0,'name']} com Regra: {rule.loc[0,'name']}",
#                     "create": association_create
#                 }, 
#                 ensure_ascii=False
#             ),
#             mimetype="application/json",
#             status=200,
#         )
#     elif len(rule):
#         msg = 'Não existe camada para os parâmetros informados'
#     else:
#         msg = 'Não existe regra para os parâmetros informados'
#     return Response(
#         json.dumps(
#             {'msg': msg},
#             ensure_ascii=False
#         ),
#         mimetype="application/json",
#         status=422,
#     )


from dataclasses import dataclass
import pandas as pd
from typing import Literal, Union
from src.interface_adapters.database.controllers.motor import Motorinterface
from src.interface_adapters.schemas.motor.association import (
    BodyAssociationLayersPolicys,
    PathAssociation,
    PathLayersPolicys,
    PathRulesLayers,
    BodyPrioritys,
    BodyAssociationRulesLayers,
    QueryUpdateAssociationRulesLayers
)


@dataclass
class Association:
    motor: Motorinterface


    def get_all_association(self, type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Rota GET para acessar todas as Associações Camadas com Política
        """
        if type_association == 'layers_to_policys':
            association = self.motor.get_all_association_layer_to_police().to_dict(orient='records')
        else:
            association = self.motor.get_all_association_rule_to_layer().to_dict(orient='records')
        return association

    def get_association_by_id(self, path: Union[PathLayersPolicys, PathRulesLayers], type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Rota GET para acessar a Associação Camadas com Política por id
        """
        if type_association == 'layers_to_policys':
            association = (
                self.motor
                .get_association_layer_to_police_by_id(path.type_id, [path.index_id])
                .sort_values('priority')
                .to_dict(orient='records')
            )
        else:
            association = (
                self.motor
                .get_association_rule_to_layer_by_id(path.type_id, [path.index_id])
                .to_dict(orient='records')
            )
        return association
    
    def delete_association(self, path: PathAssociation, type_association: Literal['layers_to_policys', 'rules_to_layers']) -> list[dict]:
        """
        Rota DELETE para deletar as Associações por id
        """
        if type_association == 'layers_to_policys':
            association = self.motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
        else:
            association = self.motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
        if len(association):
            data_update = association.copy()
            data_update['status'] = 'inactive'
            data_update.rename(columns={'association_id': 'id'}, inplace=True)
            self.motor.update_item(type_association, data_update.to_dict(orient='records'))
        return association.to_dict(orient='records')

    def associate_layers_to_policys(self, body: BodyAssociationLayersPolicys) -> list[dict]:
        """
        Rota POST para adicionar nova Associação Camadas com Política
        """
        policy = self.motor.get_policys_by_id([body.policy_id])
        layer = self.motor.get_layers_by_id([body.layer_id])
        other_layers_association = (
            self.motor
            .get_association_layer_to_police_by_id('policy_id', [body.policy_id])
        )
        if len(policy) and len(layer):
            layers_to_policys = self.motor.get_all_association_layer_to_police(status='inactive')
            layers_to_policys_update = layers_to_policys.query(f'layer_id == {body.layer_id} and policy_id == {body.policy_id}')
            if len(layers_to_policys_update):
                layers_to_policys_update["priority"] = len(other_layers_association)
                layers_to_policys_update['status'] = 'active'
                layers_to_policys_update.rename(columns={'association_id':'id'}, inplace=True)
                self.motor.update_item('layers_to_policys', layers_to_policys_update.to_dict(orient='records'))
                id_save = layers_to_policys_update['id'].to_list()
            else:
                data_save = {
                    'id': None,
                    'policy_id': body.policy_id,
                    'layer_id': body.layer_id,
                    'priority': len(other_layers_association)
                }
                id_save = self.motor.add_item('layers_to_policys', [data_save])
            association_create = (
                self.motor
                .get_association_layer_to_police_by_id('association_id', id_save)
                .to_dict(orient='records')
            )
            return association_create
        if len(policy):
            raise SyntaxError("The specified layer does not exist.")
        raise SyntaxError("The specified policy does not exist.")

    def associate_rules_to_layers(self, body: BodyAssociationRulesLayers) -> list[dict]:
        """
        Rota POST para adicionar nova Associação Regras com Camada
        """
        layer = self.motor.get_layers_by_id([body.layer_id])
        rule = self.motor.get_rules_by_id([body.rule_id])
        if len(rule) and len(layer):
            rule_to_layer = self.motor.get_all_association_rule_to_layer(status='inactive')
            rule_to_layer_update = rule_to_layer.query(f'layer_id == {body.layer_id} and rule_id == {body.rule_id}')
            if len(rule_to_layer_update): 
                rule_to_layer_update["action"] = body.action
                rule_to_layer_update['status'] = 'active'
                rule_to_layer_update.rename(columns={'association_id': 'id'}, inplace=True)
                self.motor.update_item('rules_to_layers', rule_to_layer_update.to_dict(orient='records'))
                id_save = rule_to_layer_update['id'].to_list()
            else:
                data_save = {
                    'id': None,
                    "layer_id": body.layer_id,
                    "rule_id": body.rule_id,
                    "action": body.action
                }
                id_save = self.motor.add_item('rules_to_layers', [data_save])
            association_create = (
                self.motor
                .get_association_rule_to_layer_by_id('association_id', id_save)
                .to_dict(orient='records')
            )
            return association_create
        elif len(rule):
            raise SyntaxError('Não existe camada para os parâmetros informados')
        raise SyntaxError('Não existe regra para os parâmetros informados')

    def alter_priority_layers_to_policys(self, body: BodyPrioritys) -> list[dict]:
        """
        Rota POST responsável por alterar as prioridades das camadas na Associação Camadas com Política
        """
        itens = []
        association_id = []
        
        
        for item in body.prioritys:
            itens.append(item.model_dump())
            association_id.append(item.association_id)

        association = self.motor.get_all_association_layer_to_police()
        if association.query('association_id in @association_id')['policy_id'].nunique() > 1:
            raise SyntaxError("Sorting can only be done one policy at a time.")
        policy_id = association.query('association_id in @association_id')['policy_id'].unique()
        itens_not_informed = (
            association
            .query('policy_id in @policy_id')
            .query('association_id not in @association_id')['association_id']
            .to_list()
        )
        if itens_not_informed:
            raise SyntaxError("All layer IDs linked to the policy must be provided.")

        prioritys = pd.DataFrame(itens)
        prioritys = prioritys.sort_values(['priority', 'association_id']).reset_index(drop=True)
        prioritys['priority'] = prioritys.index
        self.motor.update_item('layers_to_policys', prioritys.rename(columns={'association_id': 'id'}).to_dict(orient='records'))
        return prioritys.to_dict(orient='records')
    
    def update_rules_to_layers(self, path: PathAssociation, query: QueryUpdateAssociationRulesLayers):
        previous_association = self.motor.get_association_rule_to_layer_by_id('association_id', [path.association_id])
        if len(previous_association):
            data_update = {key: value for key, value in query.model_dump().items() if value is not None}
            data_update['id'] = path.association_id
            self.motor.update_item('rules_to_layers', [data_update])
            update_association = self.motor.get_association_layer_to_police_by_id('association_id', [path.association_id])
            return (
                previous_association.to_dict(orient='records'), 
                update_association.to_dict(orient='records')
            )
        raise SystemError('Association does not exist.')