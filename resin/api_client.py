import time
from dataclasses import dataclass
from enum import Enum
from typing import Any
from urllib.parse import urlencode, urlparse, urlunparse

import requests


@dataclass
class Entity:
    name: str
    api_path: str


type EntitySet = list[Entity]

api_entities: EntitySet = [
    Entity("fund", "funds"),
    Entity("project", "projects"),
    Entity("person", "persons"),
    Entity("organisation", "organisations"),
    Entity("artisticAndCreativeProduct", "outcomes/artisticandcreativeproducts"),
    Entity("collaboration", "outcomes/collaborations"),
    Entity("dissemination", "outcomes/disseminations"),
    # WARN: the response is missing an R so we use "futherfunding" rather than "furtherfunding"
    Entity("futherfunding", "outcomes/furtherfundings"),
    Entity("impactSummary", "outcomes/impactsummaries"),
    Entity("intellectualProperty", "outcomes/intellectualproperties"),
    Entity("keyFinding", "outcomes/keyfindings"),
    Entity("policyInfluence", "outcomes/policyinfluences"),
    Entity("product", "outcomes/products"),
    Entity("researchDatabaseAndModel", "outcomes/researchdatabaseandmodels"),
    Entity("researchMaterial", "outcomes/researchmaterials"),
    Entity(
        "softwareAndTechnicalProduct",
        "outcomes/softwareandtechnicalproducts",
    ),
    Entity("spinOut", "outcomes/spinouts"),
    Entity("publication", "outcomes/publications"),
]


class ApiClientMessage(Enum):
    RateLimitExceeded = "Rate limit exceeded. Waiting for {delay} seconds"
    ServiceUnavailable = "Service unavailable. Waiting for {delay} seconds"

    def __call__(self, **kwargs: Any) -> str:
        return self.value.format(**kwargs)


class ApiClientError(Exception):
    """Base exception for API client errors."""

    pass


class RateLimitError(ApiClientError):
    """Raised when rate limit (429) is encountered."""

    def __init__(self):
        super().__init__("Rate limit exceeded after maximum retries")


class ServiceUnavailableError(ApiClientError):
    """Raised when service unavailable (503) is encountered."""

    def __init__(self):
        super().__init__("Service unavailable after maximum retries")


class ApiClient:
    """Client for fetching data from the GTR API."""

    MAX_RETRIES = 3
    RETRY_DELAY = 300
    DEFAULT_TIMEOUT = 30

    def __init__(self, base_url: str = "https://gtr.ukri.org/gtr/api"):
        self.base_url = urlparse(base_url)
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "User-Agent": "resin-fetcher/1.0"}
        )

    def make_url(self, api_path: str, page: int) -> str:
        """Construct URL for GTR API request."""
        updated_url = self.base_url._replace(
            path=f"{self.base_url.path}/{api_path}",
            query=urlencode({"p": page, "s": 100}),
        )
        return urlunparse(updated_url)

    def _fetch_page(
        self, api_path: str, page: int, timeout: int = DEFAULT_TIMEOUT
    ) -> dict[str, Any]:
        """
        Fetch a single page of data from the API.

        Args:
            api_path: API endpoint path (e.g., "funds", "projects")
            page: Page number to fetch
            timeout: Request timeout in seconds

        Returns:
            Parsed JSON response as dict

        Raises:
            requests.RequestException: For HTTP errors, timeouts, etc.
        """
        url = self.make_url(api_path, page)

        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()

        return response.json()

    def fetch_page(self, api_path: str, page: int) -> dict[str, Any]:
        """
        Fetch a single page with retry logic matching current fetcher behavior.

        Args:
            api_path: API endpoint path (e.g., "funds", "projects")
            page: Page number to fetch

        Returns:
            Parsed JSON response as dict

        Raises:
            ApiClientError: After max retries exceeded
        """
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                return self._fetch_page(api_path, page)
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    if attempt < self.MAX_RETRIES:
                        print(
                            ApiClientMessage.RateLimitExceeded(delay=self.RETRY_DELAY)
                        )
                        time.sleep(self.RETRY_DELAY)
                        continue
                    raise RateLimitError()
                elif e.response.status_code == 503:
                    if attempt < self.MAX_RETRIES:
                        print(
                            ApiClientMessage.ServiceUnavailable(delay=self.RETRY_DELAY)
                        )
                        time.sleep(self.RETRY_DELAY)
                        continue
                    raise ServiceUnavailableError()
                else:
                    raise ApiClientError(f"HTTP error: {e}")

        raise ApiClientError(f"Max retries ({self.MAX_RETRIES}) exceeded")

    def close(self):
        """Close the HTTP session."""
        self.session.close()
