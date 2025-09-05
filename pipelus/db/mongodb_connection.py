from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database


class MongoDBConnection:
    """Gerencia a conexão com um banco MongoDB."""

    def __init__(self, connection_string: str, db_name: str) -> None:
        """Inicializa a classe MongoDBConnection."""
        self.connection_string: str = connection_string
        self.db_name: str = db_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None

    def __enter__(self) -> Database:
        """Abre a conexão com o MongoDB e retorna o objeto do banco."""
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão com o MongoDB ao sair do contexto."""
        if self.client:
            self.client.close()
