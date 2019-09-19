import requests
from .utils import PositionData
from .urls import UNIPOLSAI_BASE, LOGIN_URL, HOME_URL, POST_LOGIN, API_URL

class Unipolsai:
    def __init__(self, creds: dict, headers:dict):
        self.creds = creds
        self.session = requests.session()
        self.session.headers.update(headers)
        self.is_authenticated = False

    def authenticate(self):
        self.session.head(UNIPOLSAI_BASE)
        self.session.post(UNIPOLSAI_BASE + LOGIN_URL, data=self.creds)
        self.session.head(UNIPOLSAI_BASE + HOME_URL)
        self.is_authenticated = self._check_auth()

    def get_position(self, plate:str, update:bool) -> PositionData:
        self.is_authenticated = self._check_auth()
        if not self.is_authenticated:
            self.authenticate()
        response = self.session.get(
            url=UNIPOLSAI_BASE + API_URL.format(plate=str(plate).upper(),
                                                update=str(update).lower())
        )
        if response.status_code == 200:
            if response.json().get("operationResult").get("type") == 0:
                raw_position = response.json().get('lastPosition')
                parsed_position = PositionData.parse_raw_position(raw_position)
                return parsed_position
        else:
            print(str(response.status_code) + str(response.content))

    def _check_auth(self):
        response = self.session.post(
            url=UNIPOLSAI_BASE + POST_LOGIN,
            data={'channel': "TPD_Web"})
        return response.status_code == 200

    def __del__(self):
        self.session.close()