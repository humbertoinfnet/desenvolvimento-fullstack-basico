from typing import Literal
import pandas as pd
from sqlalchemy import exc
from src.interface_adapters.database.controllers.motor import Motorinterface
from src.external_interfaces.database.model.motor import (
    LayerRuleAssociation,
    PolicyLayerAssociation,
    Layers,
    Policys,
    Rules
)


class Motor(Motorinterface):
    
    def get_all_policys(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Policys.id.label('policy_id'),
                    Policys.name,
                    Policys.description,
                    Policys.identify
                )
                .filter(Policys.status == status)                
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def get_policys_by_id(self, policys_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Policys.id.label('policy_id'),
                    Policys.name,
                    Policys.description,
                    Policys.identify
                )
                .filter(Policys.status == 'active')                
                .filter(Policys.id.in_(policys_id))                
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def get_all_layers(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Layers.id.label('layer_id'),
                    Layers.name,
                    Layers.description,
                    Layers.identify
                )
                .filter(Layers.status == status)              
                      
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def get_layers_by_id(self, layers_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Layers.id.label('layer_id'),
                    Layers.name,
                    Layers.description,
                    Layers.identify
                )
                .filter(Layers.status == 'active')
                .filter(Layers.id.in_(layers_id))
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def get_all_rules(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Rules.id.label('rule_id'),
                    Rules.name,
                    Rules.code,
                    Rules.description,
                    Rules.identify,
                    Rules.rule
                )
                .filter(Rules.status == status)                
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def get_rules_by_id(self, rules_id: list) -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Rules.id.label('rule_id'),
                    Rules.name,
                    Rules.code,
                    Rules.description,
                    Rules.identify,
                    Rules.rule
                )
                .filter(Rules.status == 'active')                
                .filter(Rules.id.in_(rules_id))                
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)
    
    def get_all_association_rule_to_layer(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    LayerRuleAssociation.id.label('association_id'),
                    Layers.name.label('name_layer'),
                    Rules.name.label('name_rule'),
                    LayerRuleAssociation.layer_id,
                    LayerRuleAssociation.rule_id,
                    LayerRuleAssociation.action,
                    LayerRuleAssociation.identify
                )
                .join(Layers, Layers.id==LayerRuleAssociation.layer_id)
                .join(Rules, Rules.id==LayerRuleAssociation.rule_id)
                .filter(LayerRuleAssociation.status == status)  
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)
  
    def get_association_rule_to_layer_by_id(self, type_id: Literal['association_id', 'layer_id', 'rule_id'], index_ix: list[int]) -> pd.DataFrame:
        column_index = {
            'layer_id': LayerRuleAssociation.layer_id,
            'rule_id': LayerRuleAssociation.rule_id
        }.get(type_id,  LayerRuleAssociation.id)

        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    LayerRuleAssociation.id.label('association_id'),
                    Layers.name.label('name_layer'),
                    Rules.name.label('name_rule'),
                    LayerRuleAssociation.layer_id,
                    LayerRuleAssociation.rule_id,
                    LayerRuleAssociation.action,
                    LayerRuleAssociation.identify
                )
                .join(Layers, Layers.id==LayerRuleAssociation.layer_id)
                .join(Rules, Rules.id==LayerRuleAssociation.rule_id)
                .filter(LayerRuleAssociation.status == 'active')
                .filter(column_index.in_(index_ix))
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)
  
    def get_all_association_layer_to_police(self, status: Literal['active', 'inactive'] = 'active') -> pd.DataFrame:
        columns = []
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    PolicyLayerAssociation.id.label('association_id'),
                    Layers.name.label('name_layer'),
                    Policys.name.label('name_policy'),
                    PolicyLayerAssociation.policy_id,
                    PolicyLayerAssociation.layer_id,
                    PolicyLayerAssociation.priority,
                    PolicyLayerAssociation.identify
                )
                .join(Layers, Layers.id==PolicyLayerAssociation.layer_id)
                .join(Policys, Policys.id==PolicyLayerAssociation.policy_id)
                .filter(PolicyLayerAssociation.status == status)         
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)
    
    def get_association_layer_to_police_by_id(self, type_id: Literal['association_id', 'policy_id', 'layer_id'], index_ix: list[int]) -> pd.DataFrame:
        column_index = {
            'policy_id': PolicyLayerAssociation.policy_id,
            'layer_id': PolicyLayerAssociation.layer_id
        }.get(type_id,  PolicyLayerAssociation.id)
        
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    PolicyLayerAssociation.id.label('association_id'),
                    Layers.name.label('name_layer'),
                    Policys.name.label('name_policy'),
                    PolicyLayerAssociation.policy_id,
                    PolicyLayerAssociation.layer_id,
                    PolicyLayerAssociation.priority,
                    PolicyLayerAssociation.identify
                )
                .join(Layers, Layers.id==PolicyLayerAssociation.layer_id)
                .join(Policys, Policys.id==PolicyLayerAssociation.policy_id)
                .filter(PolicyLayerAssociation.status == 'active')
                .filter(column_index.in_(index_ix))
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)
    
    def add_item(self, name_table: str, data_save: list[dict]) -> list:
        try:
            table = self.get_table(name_table)
            with self.dbconn(database_name=self.database) as conn:
                items_save = [table(**params) for params in data_save]
                conn.session.bulk_save_objects(items_save, return_defaults=True)
                conn.session.commit()
                ids_save = [r.id for r in items_save]
            return ids_save
        except exc.IntegrityError:
            raise SyntaxError('Record already exists.')
        except Exception:
            raise SyntaxError('Error saving to the database.')
    
    def update_item(self, name_table: str, data_update: list[dict]):
        try:
            table = self.get_table(name_table)
            with self.dbconn(database_name=self.database) as conn:
                conn.session.bulk_update_mappings(table, data_update)
                conn.session.commit()
        except exc.IntegrityError:
            raise SyntaxError('Record already exists.')
        except Exception:
            raise SyntaxError('Error saving to the database.')

    @classmethod
    def get_table(cls, name_table):
        return {
            'policys': Policys,
            'layers': Layers,
            'rules': Rules,
            'rules_to_layers': LayerRuleAssociation,
            'layers_to_policys': PolicyLayerAssociation,
        }.get(name_table)