import logging
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import TextClause, create_engine, text
from sqlalchemy.engine import Connection, Engine, Result
from sqlalchemy.exc import SQLAlchemyError

from pipelus.db.base_connection import SyncBaseConnectionWithExecute


class SyncSQLiteConnection(SyncBaseConnectionWithExecute):
    """Gerencia a conexão síncrona com um banco de dados SQLite."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe SyncSQLiteConnection."""
        super().__init__(connection_string)
        self.engine: Engine = create_engine(
            self.connection_string, echo=False, future=True
        )

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa uma query de leitura (SELECT) no SQLite e retorna os resultados."""
        if not self.connection:
            logging.error("Conexão não está aberta. Use 'with'.")

        try:
            logging.debug('Executando query no SQLite.')
            result: Result = self.connection.execute(text(query))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            logging.info(
                f'Query executada com sucesso. Linhas retornadas: {len(data)}'
            )
            return data
        except SQLAlchemyError as e:
            logging.error(f'Erro ao executar query no SQLite: {str(e)}')
            return []

    def execute_modify(self, query: str) -> bool:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE) no SQLite."""
        if not self.engine:
            logging.error("Conexão não está aberta. Use 'with'.")

        try:
            logging.debug('Executando modificação no SQLite.')
            with self.engine.begin() as conn:
                if isinstance(query, TextClause):
                    conn.execute(query)
                else:
                    conn.execute(text(query))
            logging.info(
                'Query de modificação executada com sucesso no SQLite.'
            )
            return True
        except SQLAlchemyError as e:
            logging.error(
                f'Erro ao executar modificação no SQLite. Rollback realizado: {str(e)}'
            )
            return False
