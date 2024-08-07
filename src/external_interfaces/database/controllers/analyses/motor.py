from typing import Literal, Union
import pandas as pd
from flask import current_app
from sqlalchemy import exc
from src.interface_adapters.database.controllers.analyses import Motorinterface
from src.external_interfaces.database.model.motor import (
    LayerRuleAssociation,
    PolicyLayerAssociation,
    Layers,
    Policys,
    Rules,
    Analyses
)


class Motor(Motorinterface):
    
    def get_policy_rule(self, policy_name: str) -> pd.DataFrame:
        """Método responsável por buscar a política associada ao nome.
        """

        current_app.logger.info('[Motor] - executa metodo get_all_policys')
        with self.dbconn(database_name=self.database) as conn:
            query = (
                conn.session.query(
                    Policys.id.label('policy_id'),
                    Policys.name,
                    PolicyLayerAssociation.layer_id,
                    Layers.name.label('layer_name'),
                    LayerRuleAssociation.rule_id,
                    LayerRuleAssociation.action,
                    Rules.name.label('rule_name'),
                    Rules.code,
                    Rules.rule,
                    Rules.description,
                )
                .join(PolicyLayerAssociation, PolicyLayerAssociation.policy_id == Policys.id)
                .join(LayerRuleAssociation, LayerRuleAssociation.layer_id == PolicyLayerAssociation.id)
                .join(Layers, Layers.id == PolicyLayerAssociation.layer_id)
                .join(Rules, Rules.id == LayerRuleAssociation.rule_id)
                .filter(Policys.name == policy_name)
                .filter(Policys.status == 'active')
                .filter(Rules.status == 'active')
                .filter(Layers.status == 'active')
            )
            columns = [col.get('name') for col in query.column_descriptions]
            data = query.all()
        return pd.DataFrame(data, columns=columns)

    def add_item_analyses(self, data_save: list[dict]) -> list:
        """Método responsável por salvar novos registros em banco

        Raises:
            exc.IntegrityError: gera uma exceção de registros duplicados em banco
            Exception: gera uma exceção por qualquer erro na execução do método
        """

        current_app.logger.info('[Motor] - executa metodo add_item')
        try:
            with self.dbconn(database_name=self.database) as conn:
                items_save = [Analyses(**params) for params in data_save]
                conn.session.bulk_save_objects(items_save, return_defaults=True)
                conn.session.commit()
                ids_save = [r.id for r in items_save]
            return ids_save
        except exc.IntegrityError as err:
            current_app.logger.error(f'[Motor] - executa metodo add_item - erro: {err}')
            raise SyntaxError('Record already exists.')
        except Exception as err:
            current_app.logger.error(f'[Motor] - executa metodo add_item - erro: {err}')
            raise SyntaxError('Error saving to the database.')