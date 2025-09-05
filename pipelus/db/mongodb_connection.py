import logging
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
