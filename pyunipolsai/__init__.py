"""
Questo script ti permette di trovare la posizione della tua auto,
assicurata con UnipolSai compresa di Unibox (localizzatore GPS)

Guarda la documentazione per vedere come iniziare ad usare questa libreria
https://github.com/ExalFabu/pyunipolsai
"""
from .secrets import CREDS, HEADERS
from .unipolsai import Unipolsai
import logging

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def check_secrets_integrity() -> bool:
    """
    Checks if every variable in secrets.py
    :return: True if every variable in secrets.py is set
    :raises: AttributeError if one variable isn't set
    TODO: at least check if they aren't the sample value I put in the template, at least
    """
    if (CREDS.get("username") and CREDS.get("password") and HEADERS.get('api_key') and
            HEADERS.get('x-ibm-client-id') and HEADERS.get('x-ibm-client-secret') and HEADERS.get('company_id') and
            HEADERS.get('service_type')):
        logger.debug("secrets.py has all variable set, at least.")
        return True
    raise AttributeError("INSERT ERROR ABOUT BAD CREDENTIALS ATTRIBUTE")


def authenticate(credentials: dict = CREDS, headers: dict = HEADERS) -> Unipolsai:
    """
    This method creates an instance of the class Unipolsai with the credentials that are already on secrets.py
    :param credentials: dict with username and password
    :param headers: headers needed to authorize the operations
    :return: Unipolsai API object already authenticated
    :type: Unipolsai
    """
    if check_secrets_integrity():
        uni = Unipolsai(credentials, headers)
        uni.authenticate()
        logger.info("Succesfully authenticated")
        return uni
