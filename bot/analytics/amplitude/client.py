from __future__ import annotations

import orjson
from aiohttp import ClientSession
from loguru import logger

from bot.analytics.types import AbstractAnalyticsLogger, BaseEvent

AMPLITUDE_ENDPOINT = "https://api2.amplitude.com/2/httpapi"


class AmplitudeTelegramLogger(AbstractAnalyticsLogger):
    def __init__(self, api_token: str, base_url: str = AMPLITUDE_ENDPOINT) -> None:
        self._api_token: str = api_token
        self._base_url: str = base_url
        self._headers = {"Content-Type": "application/json", "Accept": "*/*"}
        self._timeout = 15
        self.SUCCESS_STATUS_CODE = 200

    async def _send_request(
        self,
        event: BaseEvent,
    ) -> None:
        """Implementation of interaction with Amplitude API."""
        data = {"api_key": self._api_token, "events": [event.to_dict()]}

        async with (
            ClientSession() as session,
            session.post(
                self._base_url,
                headers=self._headers,
                data=orjson.dumps(data),
                timeout=self._timeout,
            ) as response,
        ):
            json_response = await response.json(content_type="application/json")

        self._validate_response(json_response)

    def _validate_response(self, response: dict) -> None:
        """Validate response."""
        if response.get("code") != self.SUCCESS_STATUS_CODE:
            error = response.get("error")
            code = response.get("code")

            logger.error(f"get error from amplitude api | error: {error} | code: {code}")
            msg = f"Error in amplitude api call | error: {error} | code: {code}"
            raise ValueError(msg)

        logger.info(f"successfully send to Amplitude | server_upload_time: {response['server_upload_time']}")

    async def log_event(
        self,
        event: BaseEvent,
    ) -> None:
        """Use this method to sends event to Amplitude."""
        await self._send_request(event)
