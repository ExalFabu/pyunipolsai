import requests
from pyunipolsai.utils import PositionData
from pyunipolsai.urls import UNIPOLSAI_BASE, LOGIN_URL, HOME_URL, POST_LOGIN, API_URL


class Unipolsai:
    def __init__(self, creds: dict, headers: dict):
        """Define Unipolsai object

        :param creds: dict with username and password
        :param headers: dict with headers needed to authenticate, see documentation.
        """
        self.creds = creds
        self.session = requests.session()
        self.session.headers.update(headers)
        self.is_authenticated = False

    def authenticate(self):
        """Authenticate the instance on the site
        :return: True if authentication was succesfull
        """
        self.session.head(UNIPOLSAI_BASE)
        self.session.post(UNIPOLSAI_BASE + LOGIN_URL, data=self.creds)
        self.session.head(UNIPOLSAI_BASE + HOME_URL)
        self._check_auth()
        if not self.is_authenticated:
            raise ConnectionError("There was some error connecting to the API")
        return self.is_authenticated

    def get_position(self, plate: str, update: bool) -> PositionData:
        """Get the latest position retrieved from the GPS Unibox

        :param plate: plate of the car you want to locate
        :param update: if True it will request an update of the position. In a couple of minutes or less it should be updated
        :return: PositionData object with the last position retrieved
        """
        if not self._check_auth():
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
        self.is_authenticated = response.status_code == 200
        return self.is_authenticated

    def __del__(self):
        try:
            response = self.session.get(UNIPOLSAI_BASE + "myportal/logout", headers={"Connection": "close"})
        except requests.ConnectionError:
            pass
        self.session.close()
