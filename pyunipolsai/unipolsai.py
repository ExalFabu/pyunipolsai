import logging
import time

import requests

from .urls import UNIPOLSAI_BASE, LOGIN_URL, HOME_URL, POST_LOGIN, API_URL
from .utils import PositionData
from .secrets import PLATE

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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

    def get_position(self, plate: str = PLATE, update: bool = False):
        """Get the latest position retrieved from the GPS Unibox

        :param plate: plate of the vehicle you want to locate
        :param update: if True it will request an update of the position and start a polling waiting for a new position
        :return: PositionData object with the last position retrieved
        """
        if not plate:
            raise AttributeError("If PLATE is not set in secrets.py you have to pass it as an argument")
        if not self._check_auth():
            self.authenticate()
        response = self.session.get(
            url=UNIPOLSAI_BASE + API_URL.format(plate=str(plate).upper(),
                                                update=str(update).lower())
        )
        if response.ok:
            if response.json().get("operationResult").get("type") == 0:
                raw_position = response.json().get('lastPosition')
                parsed_position = PositionData.parse_raw_position(raw_position)
                if update:
                    new_position = self._poll_position(plate=plate, last_position=parsed_position)
                    if new_position is None:
                        logger.warning("Requested updated position, couldn't return it. (Probably needed more time)")
                        logger.debug(str(parsed_position))
                        return parsed_position
                    logger.info("Requested updated position, returned it.")
                    logger.debug(str(new_position))
                    return new_position
                logger.info("Requested position without updating")
                return parsed_position
        else:
            print(str(response.status_code) + str(response.content))

    def _check_auth(self) -> bool:
        """Check if authentication was succesfull or not
        :return: True if authentication was succesfull, False if not
        """
        response = self.session.post(
            url=UNIPOLSAI_BASE + POST_LOGIN,
            data={'channel': "TPD_Web"})
        self.is_authenticated = response.status_code == 200
        if not self.is_authenticated:
            logger.error("Authentication failed: {}".format(response.content))
        return self.is_authenticated

    def _poll_position(self, plate: str, last_position: PositionData, initial_delay: int = 40, delay: int = 12,
                       backoff=1, tries: int = 5):
        import datetime
        """ This method polls the api to see if the position is changed since the update request

        :param plate: Plate of the vehicle
        :param last_position: Last position of the vehicle
        :param initial_delay: Seconds to wait before starting the polling
        :param delay: Seconds to wait after each try
        :param backoff: Multiplier for the delay
        :param tries: Number of tries
        :return: The new location if found, None if not able to get a different position
        """
        now = datetime.datetime.now().timestamp()
        ten_min_ago = str(now - (10 * 60))[:10]
        if ten_min_ago < last_position.unix_timestamp:
            logger.debug("5m ago: {} | lastPos: {}".format(ten_min_ago, last_position.unix_timestamp))
            logger.info("Requested an update too soon, returning the last position")
            # since the api won't respond I just skip that and return it instantly
            return last_position
        logger.debug("Waiting initial {} seconds".format(initial_delay))
        time.sleep(initial_delay)
        for n in range(tries):
            try:
                new_position = self.get_position(plate)
                if new_position.unix_timestamp == last_position.unix_timestamp:
                    logger.debug("#{}. Still not updated. Delay: {}".format(n, delay))
                    time.sleep(delay)
                    delay = int(delay * backoff)
                else:
                    logger.debug("Found new position on #{} after {} seconds".format(n, initial_delay + delay))
                    return new_position
            except AttributeError as a_e:
                logger.warning("Attribute Error: {}".format(a_e))
                pass
            except ConnectionError as c_e:
                logger.warning("Connection Error: {}".format(c_e))
        return None

    def __del__(self):
        logger.debug("Logging off")
        try:
            response = self.session.get(UNIPOLSAI_BASE + "myportal/logout", headers={"Connection": "close"})
        except requests.ConnectionError:
            # Don't really understand this
            pass
        logger.info("Succesfully logged off")
        self.session.close()
