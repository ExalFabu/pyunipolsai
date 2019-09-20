from .unipolsai import Unipolsai
from .secrets import CREDS, HEADERS


def authenticate(credentials: dict=CREDS, headers: dict=HEADERS) -> Unipolsai:
    if credentials.get("username") and credentials.get("password"):
        uni = Unipolsai(credentials, headers)
        uni.authenticate()
        return uni
    raise AttributeError("INSERT ERROR ABOUT BAD CREDENTIALS ATTRIBUTE")