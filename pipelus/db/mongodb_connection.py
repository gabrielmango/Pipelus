import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database

from pipelus.db.base_connection import SyncBaseConnection


class MongoDBConnection(SyncBaseConnection):
    """Gerencia a conexão com um banco MongoDB."""

    def __init__(self, connection_string: str, db_name: str) -> None:
        """Inicializa a classe MongoDBConnection."""
        super().__init__(connection_string)
        self.db_name: str = db_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None

    def __enter__(self) -> Database:
        """Abre a conexão com o MongoDB e retorna o objeto do banco."""
        try:
            logging.info(f'Conectando ao MongoDB: {self.db_name}')
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            logging.info(f'Conexão estabelecida com o banco {self.db_name}')
            return self.db
        except Exception as e:
            logging.error(
                f'Erro ao conectar ao MongoDB: {self.db_name} - {str(e)}'
            )
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão com o MongoDB ao sair do contexto."""
        if self.client:
            try:
                self.client.close()
                logging.info(
                    f'Conexão com o banco {self.db_name} encerrada com sucesso'
                )
            except Exception as e:
                logging.error(f'Erro ao fechar conexão com MongoDB: {str(e)}')


class AsyncMongoDBConnection:
    """Gerencia a conexão assíncrona com um banco MongoDB."""

    def __init__(self, connection_string: str, db_name: str) -> None:
        """Inicializa a classe AsyncMongoDBConnection."""
        self.connection_string: str = connection_string
        self.db_name: str = db_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None

    async def __aenter__(self) -> AsyncIOMotorDatabase:
        """Abre a conexão assíncrona com o MongoDB e retorna o objeto do banco."""
        try:
            logging.info(f'Conectando ao MongoDB: {self.db_name}')
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.db_name]
            logging.info(f'Conexão estabelecida com o banco {self.db_name}')
            return self.db
        except Exception as e:
            logging.error(
                f'Erro ao conectar ao MongoDB: {self.db_name} - {str(e)}'
            )
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão assíncrona com o MongoDB ao sair do contexto."""
        if self.client:
            try:
                self.client.close()
                logging.info(
                    f'Conexão com o banco {self.db_name} encerrada com sucesso'
                )
            except Exception as e:
                logging.error(f'Erro ao fechar conexão com MongoDB: {str(e)}')
