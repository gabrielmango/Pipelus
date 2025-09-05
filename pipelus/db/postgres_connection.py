import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import TextClause, create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError


class PostgresConnection:
    """Gerencia a conexão com um banco PostgreSQL."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe PostgresConnection."""
        self.connection_string: str = connection_string
        self.engine = create_engine(self.connection_string)
        self.connection: Optional[Connection] = None

    def __enter__(self) -> 'PostgresConnection':
        """Abre a conexão com o PostgreSQL ao entrar no contexto."""
        try:
            logging.info('Abrindo conexão com PostgreSQL...')
            self.connection = self.engine.connect()
            logging.info('Conexão estabelecida com PostgreSQL.')
            return self
        except Exception as e:
            logging.error(f'Erro ao conectar ao PostgreSQL: {str(e)}')
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão ao sair do contexto."""
        if self.connection:
            try:
                self.connection.close()
                logging.info('Conexão com PostgreSQL encerrada com sucesso.')
            except Exception as e:
                logging.error(
                    f'Erro ao fechar conexão com PostgreSQL: {str(e)}'
                )

    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executa uma query de leitura (SELECT) e retorna os resultados."""
        try:
            logging.debug('Executando query.')
            result = self.connection.execute(text(query), params or {})
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            logging.info(
                f'Query executada com sucesso. Linhas retornadas: {len(data)}'
            )
            return data
        except SQLAlchemyError as e:
            logging.error(f'Erro ao executar query: {str(e)}')
            return []

    def execute_modify(
        self, query: str | TextClause, params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE)."""
        try:
            logging.debug('Executando modificação.')
            with self.engine.begin() as connection:
                if isinstance(query, TextClause):
                    connection.execute(query, params or {})
                else:
                    connection.execute(text(query), params or {})
            logging.info('Query de modificação executada com sucesso.')
            return True
        except SQLAlchemyError as e:
            logging.error(
                f'Erro ao executar modificação. Rollback realizado: {str(e)}'
            )
            return False
