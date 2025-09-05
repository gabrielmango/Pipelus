import inspect
import logging
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

from dotenv import load_dotenv

load_dotenv()

_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def _get_level_from_env(var_name: str, default: int = logging.INFO) -> int:
    """Recupera o nível de log a partir de uma variável de ambiente."""
    value = os.getenv(var_name, '').strip().upper()
    return _LEVELS.get(value, default)


class LoggerManager:
    """Gerencia a criação de logs para um script ou aplicação."""

    def __init__(
        self, log_name: Optional[str] = None, log_folder: str = 'logs'
    ) -> None:
        """Inicializa a classe LoggerManager"""
        if log_name is None:
            caller_file = inspect.stack()[1].filename
            log_name = os.path.splitext(os.path.basename(caller_file))[0]

        self.log_name: str = log_name
        self.log_folder: str = log_folder
        self.date_folder: str = datetime.now().strftime('%Y_%m_%d')
        self.log_file: str = (
            f'{self.log_folder}/{self.date_folder}/{self.log_name}.log'
        )

        self.level: int = _get_level_from_env('LOG_LEVEL', logging.INFO)

        self._setup_log_folder()
        self.logger: logging.Logger = self._setup_logger()

    def _setup_log_folder(self) -> None:
        """Cria a pasta de logs, caso não exista."""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Configura o logger com handlers de arquivo e console."""
        logger = logging.getLogger(self.log_name)
        logger.setLevel(self.level)
        logger.propagate = False

        if not logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )

            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(self.level)
            stream_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger

    def set_level(self, level_name: str) -> None:
        """Altera o nível de log do logger e de todos os handlers."""
        level = _LEVELS.get(level_name.strip().upper(), None)
        if level is None:
            self.logger.warning(
                f"Nível inválido '{level_name}'. Mantendo {logging.getLevelName(self.logger.level)}."
            )
            return

        self.logger.setLevel(level)
        for h in self.logger.handlers:
            h.setLevel(level)
        self.logger.info(f'Nível de log alterado para {level_name.upper()}')

    def log_execution(self, func: Callable) -> Callable:
        """Decorator que registra início, fim, duração e exceções de uma função."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
            self.logger.info('Processo iniciado.')
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                self.logger.info('Processo concluído com sucesso.')
                return result
            except Exception as e:
                self.logger.error(f'Erro inesperado: {e}', exc_info=True)
                # raise
            finally:
                duration = datetime.now() - start_time
                self.logger.info(f'Tempo de execução: {duration}')
                self.logger.info('Processo finalizado.\n')

        return wrapper
