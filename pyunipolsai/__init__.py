from .unipolsai import Unipolsai
from .utils import PositionData


def authenticate(credentials: dict, headers: dict) -> Unipolsai:
    if credentials.get("username") and credentials.get("password"):
        uni = Unipolsai(credentials, headers)
        uni.authenticate()
        return uni
    raise AttributeError("INSERT ERROR ABOUT BAD CREDENTIALS ATTRIBUTE")