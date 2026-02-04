import logging

import requests
from decouple import config

from global_utils.http_helpers import status_codes

logger = logging.getLogger(__name__)


class BaseApiHandler:

    def __init__(self, api_name: str = None):
        self.api_name = api_name or ""
        self.headers = {}
        self.url_params = {}
        self.timeout = 2

    def get(self, url: str, symbol: str, retry=3) -> dict:
        try:
            response = requests.get(url=url, headers=self.headers, timeout=self.timeout, params=self.url_params)
            if response.status_code == status_codes.HTTP_200_OK:
                return response.json()

            if response.status_code == status_codes.HTTP_404_NOT_FOUND:
                logger.error(f"Item {symbol} not found.")
                return {}
            elif response.status_code == status_codes.HTTP_400_BAD_REQUEST:
                logger.error(response.json())
                return {}
            elif response.status_code == status_codes.HTTP_402_PAYMENT_REQUIRED:
                logger.error(f"{self.api_name} API payment required or quota exceeded.")
                return {}
            elif status_codes.is_server_error(response.status_code):
                raise requests.RequestException()

        except (requests.Timeout, requests.ConnectTimeout, requests.ReadTimeout):
            logger.error(f"Request to {self.api_name} API timed out.")
            if retry > 0:
                self.get(url=url, symbol=symbol, retry=retry - 1)
            else:
                return {}
        except requests.RequestException as e:
            logger.error(f"Request to {self.api_name} API failed: {e}", exc_info=True)
            return {}
        except Exception as exc:
            logger.error(f"An unexpected error occurred: {exc}", exc_info=True)
            return {}
