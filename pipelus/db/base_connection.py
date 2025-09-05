import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine


class SyncBaseConnection(ABC):
    """Classe abstrata para conexões de banco de dados."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe."""
        self.connection_string: str = connection_string
        self.engine = None
        self.connection = None

    def __enter__(self):
        """Abre a conexão com o banco de dados."""
        try:
            self.connection = self.engine.connect()
            logging.info('Conexão estabelecida.')
            return self
        except Exception as e:
            logging.error(f'Erro ao conectar: {str(e)}')
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão ao sair do contexto."""
        if self.connection:
            try:
                self.connection.close()
                logging.info('Conexão encerrada com sucesso.')
            except Exception as e:
                logging.error(f'Erro ao fechar conexão: {str(e)}')


class SyncBaseConnectionWithExecute(SyncBaseConnection):
    """Extensão da SyncBaseConnection que define os métodos abstratos."""

    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa uma query de leitura (SELECT) e retorna os resultados."""
        pass

    @abstractmethod
    def execute_modify(self, query: str) -> bool:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE)."""
        pass


class AsyncBaseConnection(ABC):
    """Classe abstrata para conexões assíncronas de banco de dados."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe."""
        self.connection_string: str = connection_string
        self.engine: Optional[AsyncEngine] = None
        self.connection: Optional[AsyncConnection] = None

    async def __aenter__(self):
        """Abre a conexão com o banco de dados."""
        try:
            if self.engine is None:
                raise ValueError('O engine não foi inicializado.')
            self.connection = await self.engine.connect()
            logging.info('Conexão assíncrona estabelecida.')
            return self
        except Exception as e:
            logging.error(f'Erro ao conectar de forma assíncrona: {str(e)}')
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão ao sair do contexto assíncrono."""
        if self.connection:
            try:
                await self.connection.close()
                logging.info('Conexão assíncrona encerrada com sucesso.')
            except Exception as e:
                logging.error(f'Erro ao fechar conexão assíncrona: {str(e)}')
