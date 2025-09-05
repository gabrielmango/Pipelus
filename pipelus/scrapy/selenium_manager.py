import logging
from typing import Optional, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumManager:
    """Classe para gerenciar interações com o Selenium WebDriver (Chrome)."""

    def __init__(self, url: Optional[str] = None) -> None:
        """Inicializa o SeleniumManager configurando o WebDriver."""
        self._url: Optional[str] = url
        self.driver: webdriver.Chrome = self._configurar_driver()
        self.driver.implicitly_wait(2)
        logging.info('Driver Selenium configurado com sucesso.')

    def __enter__(self) -> 'SeleniumManager':
        """Entra no contexto."""
        logging.debug(
            'Entrando no gerenciador de contexto do SeleniumManager.'
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Sai do contexto, garantindo que o navegador seja fechado."""
        if exc_type:
            logging.error(f'Erro durante execução: {exc_value}', exc_info=True)
        self.fechar_pagina()
        logging.debug('Saindo do gerenciador de contexto do SeleniumManager.')

    def _configurar_driver(self) -> webdriver.Chrome:
        """Configura e retorna uma instância do WebDriver Chrome."""
        opcoes = webdriver.ChromeOptions()
        opcoes.add_argument('--start-maximized')
        opcoes.add_argument('--disable-infobars')
        opcoes.add_argument('--disable-extensions')

        servico = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=servico, options=opcoes)

    def abrir_pagina(self, url: Optional[str] = None) -> None:
        """Abre a página no navegador."""
        target_url = url or self._url
        if not target_url:
            logging.error('Nenhuma URL fornecida.')

        logging.info(f'Abrindo página: {target_url}')
        self.driver.get(target_url)
        self.espera_carregar_pagina()

    def fechar_pagina(self) -> None:
        """Fecha o navegador e encerra a sessão do WebDriver."""
        if hasattr(self, 'driver') and self.driver:
            logging.info('Fechando navegador.')
            self.driver.quit()

    def espera_carregar_pagina(self, timeout: int = 10) -> None:
        """Aguarda o carregamento da página."""
        logging.debug(
            f'Aguardando carregamento da página (timeout={timeout}s).'
        )
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

    def espera_carregar_elemento(
        self, locator: Tuple[By, str], timeout: int = 30
    ) -> WebElement:
        """Aguarda a presença de um elemento específico na página."""
        logging.debug(f'Aguardando elemento {locator} (timeout={timeout}s).')
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def trocar_para_iframe(
        self, iframe_locator: Tuple[By, str] = (By.TAG_NAME, 'iframe')
    ) -> None:
        """Troca o contexto atual para um iframe."""
        logging.info(f'Trocando para iframe localizado por {iframe_locator}.')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(iframe_locator)
        )
        iframe = self.driver.find_element(*iframe_locator)
        self.driver.switch_to.frame(iframe)

    def escrever(
        self, locator: Tuple[By, str], texto: str, timeout: int = 10
    ) -> None:
        """Localiza um campo e escreve um texto nele."""
        logging.info(f"Escrevendo no elemento {locator}: '{texto}'.")
        element = self.espera_carregar_elemento(locator, timeout)
        element.clear()
        element.send_keys(texto)

    def clicar(
        self, locator: Tuple[By, str], usar_js: bool = False, timeout: int = 30
    ) -> None:
        """Localiza e clica em um elemento."""
        logging.info(f'Clicando no elemento {locator} (usar_js={usar_js}).')
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

        if usar_js:
            self.driver.execute_script('arguments[0].click();', element)
        else:
            element.click()

        self.espera_carregar_pagina()

    def criar_locator(self, tipo: str, valor: str) -> Tuple[By, str]:
        """Cria um locator baseado em tipo e valor."""
        mapping = {
            'id': By.ID,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT,
            'name': By.NAME,
            'tag': By.TAG_NAME,
            'css': By.CSS_SELECTOR,
        }

        if tipo not in mapping:
            logging.error('Tipo de locator inválido.')

        logging.debug(f'Criando locator: tipo={tipo}, valor={valor}')
        return (mapping[tipo], valor)
