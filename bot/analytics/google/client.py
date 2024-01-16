from aiohttp import ClientSession
from loguru import logger

from bot.analytics.types import AbstractAnalyticsLogger, BaseEvent

GOOGLE_ANALYTICS_ENDPOINT = "https://www.google-analytics.com"


class GoogleAnalyticsTelegramLogger(AbstractAnalyticsLogger):
    def __init__(self, api_secret: str, measurement_id: str, base_url: str = GOOGLE_ANALYTICS_ENDPOINT) -> None:
        self._api_secret: str = api_secret
        self._measurement_id: str = measurement_id
        self._base_url: str = base_url
        self._headers = {"Content-Type": "application/json", "Accept": "*/*"}

    async def _send_request(
        self,
        event: BaseEvent,
    ) -> dict:
        url = f"{self._base_url}/mp/collect?measurement_id={self._measurement_id}&api_secret={self._api_secret}"
        params = dict(event)

        async with ClientSession() as session, session.post(url, headers=self._headers, json=params) as response:
            json_response = await response.json(content_type="application/json")

        logger.info("Send record to Google Analytics")
        logger.info(f"{json_response=}")

        return self._validate_response(json_response)

    @staticmethod
    def _validate_response(response: dict) -> dict:
        """Validate response."""
        if not response.get("ok"):
            name = response["error"]["name"]
            code = response["error"]["code"]

            logger.error(f"get error from cryptopay api | name: {name} | code: {code}")
            msg = f"Error in CryptoPay API call | name: {name} | code: {code}"
            raise ValueError(msg)

        logger.info(f"got response | ok: {response['ok']} | result: {response['result']}")
        return response

    async def log_event(
        self,
        event: BaseEvent,
    ) -> None:
        """Use this method to sends event to Google Analytics."""
        await self._send_request(event)
