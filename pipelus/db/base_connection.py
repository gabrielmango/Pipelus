import logging
from abc import ABC


class SyncBaseConnection(ABC):
    """Classe abstrata para conexões de banco de dados."""

    def __init__(self, connection_string: str) -> None:
        """Inicializa a classe."""
        self._connection_string: str = connection_string
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
