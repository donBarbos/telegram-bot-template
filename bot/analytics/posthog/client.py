from __future__ import annotations

from aiohttp import ClientSession
from loguru import logger

from bot.analytics.types import AbstractAnalyticsLogger, BaseEvent

POSTHOG_ENDPOINT = "https://app.posthog.com"


class PosthogTelegramLogger(AbstractAnalyticsLogger):
    def __init__(self, api_token: str, base_url: str = POSTHOG_ENDPOINT) -> None:
        self._api_token: str = api_token
        self._base_url: str = base_url
        self._headers = {
            "Authorization": "Bearer ${POSTHOG_PERSONAL_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "*/*",
        }
        self._timeout = 15

    async def _send_request(
        self,
        event: BaseEvent,
    ) -> dict:
        url = f"{self._base_url}/api/event/?personal_api_key={self._api_token}"
        params = dict(event)

        async with (
            ClientSession() as session,
            session.post(
                url,
                headers=self._headers,
                json=params,
                timeout=self._timeout,
            ) as response,
        ):
            json_response = await response.json(content_type="application/json")

        logger.info("Send record to Posthog")
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
        """Use this method to sends event to Posthog."""
        await self._send_request(event)
