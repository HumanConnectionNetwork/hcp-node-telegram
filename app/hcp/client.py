from typing import Any

import requests

from app.config import settings


class HCPClient:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self.base_url = (base_url or settings.hcp_node_url).rstrip("/")
        self.timeout = timeout or settings.request_timeout

    def health(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/health",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_record(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/hcp/records",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def search_reported_cases(
        self,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/hcp/search",
            params=query,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
