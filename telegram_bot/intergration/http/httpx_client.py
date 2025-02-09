from typing import Dict

import httpx
from loguru import logger

from telegram_bot.intergration.http.base_http_client import HttpClient


class HttpxClient(HttpClient):

    def __init__(self):
        transport = httpx.AsyncHTTPTransport(retries=3)
        self.client = httpx.AsyncClient(transport=transport)

    async def get(self, url: str, params: Dict = None) -> Dict:
        """
        异步请求外部资源
        """
        logger.info(f"[http][get][request]{url}")
        r = await self.client.get(url, params=params)
        logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")

        if r.status_code not in (200, 204):
            # TODO: raise Exception
            pass

        return r.json()

    async def post(self, url: str, params: Dict = None) -> Dict:
        logger.info(f"[http][post][request]{url}")
        headers = {"Content-Type": "application/json"}
        r = await self.client.post(url, json=params, headers=headers)
        logger.info(f"[http][post][response]{url},{r.status_code},{r.json()}")

        if r.status_code not in (200, 204):
            # TODO: raise Exception
            pass

        return r.json()
