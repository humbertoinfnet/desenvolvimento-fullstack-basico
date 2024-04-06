from abc import abstractclassmethod
from typing import Literal
import pandas as pd


from src.external_interfaces.database.model.motor import (
    LayerRuleAssociation,
    PolicyLayerAssociation,
    Layers,
    Policys,
    Rules
)



class Motorinterface(MotorTemplate):

    @abstractclassmethod
    def get_all_layers(self):
        raise NotImplementedError('Método não implementado')




class Motor(MotorTemplate):
    
    def get_all_policys(self) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Policys.id.label('policy_id'),
                    Policys.name,
                    Policys.description,
                    Policys.identify
                )
                .filter(Policys.status == 'active')                
            ).all()
        return pd.DataFrame(data)

    def get_policys_by_id(self, policys_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Policys.id.label('policy_id'),
                    Policys.name,
                    Policys.description,
                    Policys.identify
                )
                .filter(Policys.status == 'active')                
                .filter(Policys.id.in_(policys_id))                
            ).all()
        return pd.DataFrame(data)

    def get_all_layers(self) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Layers.id.label('layer_id'),
                    Layers.name,
                    Layers.description,
                    Layers.identify
                )
                .filter(Layers.status == 'active')              
                      
            ).all()
        return pd.DataFrame(data)

    def get_layers_by_id(self, layers_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Layers.id.label('layer_id'),
                    Layers.name,
                    Layers.description,
                    Layers.identify
                )
                .filter(Layers.status == 'active')
                .filter(Layers.id.in_(layers_id))
            ).all()
        return pd.DataFrame(data)

    def get_all_rules(self) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Rules.id.label('rule_id'),
                    Rules.name,
                    Rules.description,
                    Rules.identify
                )
                .filter(Rules.status == 'active')                
            ).all()
        return pd.DataFrame(data)

    def get_rules_by_id(self, rules_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    Rules.id.label('rule_id'),
                    Rules.code,
                    Rules.description,
                    Rules.name,
                    Rules.identify
                )
                .filter(Rules.status == 'active')                
                .filter(Rules.id.in_(rules_id))                
            ).all()
        return pd.DataFrame(data)
    
    def get_all_association_rule_to_layer(self) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    LayerRuleAssociation.id.label('association_id'),
                    LayerRuleAssociation.name_layer,
                    LayerRuleAssociation.name_rule,
                    LayerRuleAssociation.layer_id,
                    LayerRuleAssociation.rule_id,
                    LayerRuleAssociation.action,
                    LayerRuleAssociation.identify
                )
                .filter(LayerRuleAssociation.status == 'active')  
            ).all()
        return pd.DataFrame(data)
  
    def get_association_rule_to_layer_by_id(self, type_id: Literal['association_id', 'layer_id', 'rule_id'], index_ix: list[int]) -> pd.DataFrame:
        column_index = {
            'layer_id': LayerRuleAssociation.layer_id,
            'rule_id': LayerRuleAssociation.rule_id
        }.get(type_id,  LayerRuleAssociation.id)

        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    LayerRuleAssociation.id.label('association_id'),
                    LayerRuleAssociation.name_layer,
                    LayerRuleAssociation.name_rule,
                    LayerRuleAssociation.layer_id,
                    LayerRuleAssociation.rule_id,
                    LayerRuleAssociation.action,
                    LayerRuleAssociation.identify
                )
                .filter(LayerRuleAssociation.status == 'active')
                .filter(column_index.in_(index_ix))
            ).all()
        return pd.DataFrame(data)
  
    def get_all_association_layer_to_police(self) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    PolicyLayerAssociation.id.label('association_id'),
                    PolicyLayerAssociation.name_layer,
                    PolicyLayerAssociation.name_policy,
                    PolicyLayerAssociation.policy_id,
                    PolicyLayerAssociation.layer_id,
                    PolicyLayerAssociation.priority,
                    PolicyLayerAssociation.identify
                )
                .filter(PolicyLayerAssociation.status == 'active')         
            ).all()
        return pd.DataFrame(data)
    
    def get_association_layer_to_police_by_id(self, type_id: Literal['association_id', 'policy_id', 'layer_id'], index_ix: list[int]) -> pd.DataFrame:
        column_index = {
            'policy_id': PolicyLayerAssociation.policy_id,
            'layer_id': PolicyLayerAssociation.layer_id
        }.get(type_id,  PolicyLayerAssociation.id)
        
        with self.dbconn(database_name=self.database) as conn:
            data = (
                conn.session.query(
                    PolicyLayerAssociation.id.label('association_id'),
                    PolicyLayerAssociation.name_layer,
                    PolicyLayerAssociation.name_policy,
                    PolicyLayerAssociation.policy_id,
                    PolicyLayerAssociation.layer_id,
                    PolicyLayerAssociation.priority,
                    PolicyLayerAssociation.identify
                )
                .filter(PolicyLayerAssociation.status == 'active')
                .filter(column_index.in_(index_ix))
            ).all()
        return pd.DataFrame(data)
    
    def add_item(self, name_table: str, data_save: list[dict]) -> None:
        table = self.get_table(name_table)
        with self.dbconn(database_name=self.database) as conn:
            conn.session.bulk_insert_mappings(table, data_save)
            conn.session.commit()

    def update_item(self, name_table: str, data_update: list[dict]):
        table = self.get_table(name_table)
        with self.dbconn(database_name=self.database) as conn:
            conn.session.bulk_update_mappings(table, data_update)
            conn.session.commit()

    @classmethod
    def get_table(cls, name_table):
        return {
            'policys': Policys,
            'layers': Layers,
            'rules': Rules,
            'rules_to_layers': LayerRuleAssociation,
            'layers_to_policys': PolicyLayerAssociation,
        }.get(name_table)