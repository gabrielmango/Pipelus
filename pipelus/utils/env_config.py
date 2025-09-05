import logging
import os
from typing import Dict, List, Optional

from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values('.env')


class LoadEnv:
    """Classe para validar e recuperar variáveis de ambiente."""

    def __init__(self, env_variables: List[str]) -> None:
        """Inicializa a classe LoadEnv e valida as variáveis de ambiente fornecidas."""
        self._env_variables: List[str] = env_variables
        self._validate_env_variables()

    def _validate_env_variables(self) -> None:
        """Verifica se todas as variáveis de ambiente fornecidas estão definidas."""
        missing_vars: List[str] = []

        for variable in self._env_variables:
            if os.getenv(variable) is None:
                missing_vars.append(variable)

        if missing_vars:
            logging.error(f"Ausência das variáveis: {', '.join(missing_vars)}")

    def get_variables(self) -> Dict[str, Optional[str]]:
        """Retorna um dicionário contendo as variáveis de ambiente e seus valores."""
        return {var: os.getenv(var) for var in self._env_variables}
