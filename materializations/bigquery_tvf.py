# materializations/bigquery_tvf.py
from __future__ import annotations
import typing as t

import sqlglot.expressions as exp
from sqlmesh import CustomMaterialization, Model
from sqlmesh.core.macros import MacroEvaluator

if t.TYPE_CHECKING:
    from sqlmesh import QueryOrDF


def _parse_tvf_params(tvf_params: str) -> dict[str, exp.Expression]:
    """Parse 'start_date DATE, end_date DATE' into {name: Column expression}."""
    result = {}
    for param in tvf_params.split(","):
        parts = param.strip().split()
        if parts:
            name = parts[0]
            result[name] = exp.Column(this=exp.Identifier(this=name, quoted=False))
    return result


class BigQueryTVFMaterialization(CustomMaterialization):
    NAME = "bigquery_tvf"

    def create(self, table_name, model, is_table_deployable, render_kwargs, **kwargs):
        pass

    def insert(
        self,
        table_name: str,
        query_or_df: QueryOrDF,
        model: Model,
        is_first_insert: bool,
        render_kwargs: t.Dict[str, t.Any],
        **kwargs: t.Any,
    ) -> None:
        tvf_params = model.custom_materialization_properties.get("tvf_params", "")

        # Re-render the raw model query with TVF param names injected
        # as Column identifiers so they survive as bare names in the DDL
        param_vars = _parse_tvf_params(tvf_params)

        # Get the unrendered query expression from the model
        raw_query = model.render_query(**{**render_kwargs, **param_vars})

        query_sql = raw_query.sql(dialect="bigquery")
        ddl = f"""
            CREATE OR REPLACE TABLE FUNCTION `{table_name.replace('"', '')}`({tvf_params})
            AS ({query_sql})
        """
        self.adapter.execute(ddl)

    def delete(self, name: str, **kwargs: t.Any) -> None:
        self.adapter.execute(f"DROP TABLE FUNCTION IF EXISTS {name}")
