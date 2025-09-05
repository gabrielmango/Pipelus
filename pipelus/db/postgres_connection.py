import logging
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import TextClause, create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine,
                                    create_async_engine)

from pipelus.db.base_connection import (AsyncBaseConnection,
                                        SyncBaseConnectionWithExecute)


class PostgresConnection(SyncBaseConnectionWithExecute):
    """Gerencia a conexão com um banco PostgreSQL."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe PostgresConnection."""
        super().__init__(connection_string)
        self.engine: Optional[Engine] = create_engine(
            self._connection_string, echo=False, future=True
        )
        self.connection: Optional[Connection] = None

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa uma query de leitura (SELECT)."""
        try:
            result = self.connection.execute(text(query))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            logging.info(
                f'Query executada com sucesso. Linhas retornadas: {len(data)}'
            )
            return data
        except SQLAlchemyError as e:
            logging.error(f'Erro ao executar query: {str(e)}')
            return []

    def execute_modify(self, query: str) -> bool:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE)."""
        try:
            logging.debug('Executando modificação.')
            with self.engine.begin() as conn:
                if isinstance(query, TextClause):
                    conn.execute(query)
                else:
                    conn.execute(text(query))
            logging.info('Query de modificação executada com sucesso.')
            return True
        except SQLAlchemyError as e:
            logging.error(
                f'Erro ao executar modificação. Rollback realizado: {str(e)}'
            )
            return False


class AsyncPostgresConnection(AsyncBaseConnection):
    """Gerencia a conexão assíncrona com um banco PostgreSQL."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe AsyncPostgresConnection."""
        super().__init__(connection_string)
        self.engine: AsyncEngine = create_async_engine(
            self.connection_string, echo=False, future=True
        )

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa uma query de leitura (SELECT) e retorna os resultados."""
        if not self.connection:
            logging.error("Conexão não está aberta. Use 'async with'.")

        try:
            logging.debug('Executando query assíncrona no PostgreSQL.')
            result = await self.connection.execute(text(query))
            columns = result.keys()
            data = [dict(zip(columns, row)) async for row in result]
            logging.info(
                f'Query executada com sucesso. Linhas retornadas: {len(data)}'
            )
            return data
        except SQLAlchemyError as e:
            logging.error(f'Erro ao executar query: {str(e)}')
            return []

    async def execute_modify(self, query: str) -> bool:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE)."""
        if not self.engine:
            logging.error("Conexão não está aberta. Use 'async with'.")

        try:
            logging.debug('Executando modificação assíncrona no PostgreSQL.')
            async with self.engine.begin() as conn:
                if isinstance(query, TextClause):
                    await conn.execute(query)
                else:
                    await conn.execute(text(query))
            logging.info('Query de modificação executada com sucesso.')
            return True
        except SQLAlchemyError as e:
            logging.error(
                f'Erro ao executar modificação. Rollback realizado: {str(e)}'
            )
            return False
