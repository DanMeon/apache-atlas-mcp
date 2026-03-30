"""Async HTTP client for Apache Atlas REST API v2.

Wraps httpx.AsyncClient with Atlas-specific authentication,
base URL handling, and typed response methods.
"""

from typing import Any
from urllib.parse import quote

import httpx

from apache_atlas_mcp.config import AtlasSettings


def _safe(segment: str) -> str:
    """URL-encode a path segment to prevent path traversal."""
    return quote(segment, safe="")


class AtlasClient:
    """Async client for the Apache Atlas REST API v2.

    Uses HTTP Basic authentication and provides typed methods
    for each API endpoint group (entity, search, lineage, etc.).
    """

    API_PREFIX = "/api/atlas/v2"

    def __init__(self, settings: AtlasSettings) -> None:
        self._settings = settings
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=f"{self._settings.base_url}{self.API_PREFIX}",
                auth=(self._settings.username, self._settings.password),
                verify=self._settings.verify_ssl,
                timeout=self._settings.timeout,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_body: dict | list | None = None,
    ) -> Any:
        """Send a request to Atlas and return the parsed JSON response."""
        client = await self._get_client()
        try:
            response = await client.request(method, path, params=params, json=json_body)
            response.raise_for_status()
        except httpx.ConnectError as e:
            raise ValueError(
                f"Cannot connect to Atlas at {self._settings.base_url}. "
                f"Verify the server is running and ATLAS_BASE_URL is correct: {e}"
            ) from e
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            body = e.response.text[:500]
            if status == 401:
                raise ValueError(
                    "Atlas authentication failed. Check ATLAS_USERNAME and ATLAS_PASSWORD."
                ) from e
            if status == 403:
                raise ValueError(f"Access denied for {method} {path}.") from e
            if status == 404:
                raise ValueError(f"Resource not found: {path}") from e
            raise ValueError(f"Atlas API error (HTTP {status}): {body}") from e
        if response.status_code == 204:
            return {}
        return response.json()

    # * Entity endpoints

    async def get_entity_by_guid(
        self, guid: str, min_ext_info: bool = False, ignore_relationships: bool = False
    ) -> dict:
        """GET /v2/entity/guid/{guid}"""
        params = {
            "minExtInfo": str(min_ext_info).lower(),
            "ignoreRelationships": str(ignore_relationships).lower(),
        }
        return await self._request("GET", f"/entity/guid/{_safe(guid)}", params=params)

    async def get_entity_by_unique_attribute(
        self, type_name: str, attr_name: str, attr_value: str
    ) -> dict:
        """GET /v2/entity/uniqueAttribute/type/{typeName}"""
        params = {f"attr:{attr_name}": attr_value}
        return await self._request(
            "GET", f"/entity/uniqueAttribute/type/{_safe(type_name)}", params=params
        )

    async def create_or_update_entity(self, entity: dict) -> dict:
        """POST /v2/entity — create or update a single entity."""
        return await self._request("POST", "/entity", json_body={"entity": entity})

    async def delete_entity_by_guid(self, guid: str) -> dict:
        """DELETE /v2/entity/guid/{guid}"""
        return await self._request("DELETE", f"/entity/guid/{_safe(guid)}")

    async def get_entities_by_guids(self, guids: list[str]) -> dict:
        """GET /v2/entity/bulk"""
        params = {"guid": guids}
        return await self._request("GET", "/entity/bulk", params=params)

    # * Search endpoints

    async def basic_search(
        self,
        query: str | None = None,
        type_name: str | None = None,
        classification: str | None = None,
        limit: int = 25,
        offset: int = 0,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> dict:
        """GET /v2/search/basic"""
        params: dict = {"limit": limit, "offset": offset}
        if query:
            params["query"] = query
        if type_name:
            params["typeName"] = type_name
        if classification:
            params["classification"] = classification
        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order
        return await self._request("GET", "/search/basic", params=params)

    async def dsl_search(self, query: str, limit: int = 25, offset: int = 0) -> dict:
        """GET /v2/search/dsl"""
        params = {"query": query, "limit": limit, "offset": offset}
        return await self._request("GET", "/search/dsl", params=params)

    async def quick_search(self, query: str, type_name: str | None = None, limit: int = 25) -> dict:
        """GET /v2/search/quick"""
        params: dict = {"query": query, "limit": limit}
        if type_name:
            params["typeName"] = type_name
        return await self._request("GET", "/search/quick", params=params)

    # * Lineage endpoints

    async def get_lineage(self, guid: str, direction: str = "BOTH", depth: int = 3) -> dict:
        """GET /v2/lineage/{guid}"""
        params = {"direction": direction, "depth": depth}
        return await self._request("GET", f"/lineage/{_safe(guid)}", params=params)

    async def get_lineage_by_unique_attribute(
        self,
        type_name: str,
        attr_name: str,
        attr_value: str,
        direction: str = "BOTH",
        depth: int = 3,
    ) -> dict:
        """GET /v2/lineage/uniqueAttribute/type/{typeName}"""
        params = {
            f"attr:{attr_name}": attr_value,
            "direction": direction,
            "depth": depth,
        }
        return await self._request(
            "GET", f"/lineage/uniqueAttribute/type/{_safe(type_name)}", params=params
        )

    # * Classification endpoints

    async def get_classifications(self, guid: str) -> dict:
        """GET /v2/entity/guid/{guid}/classifications"""
        return await self._request("GET", f"/entity/guid/{_safe(guid)}/classifications")

    async def add_classifications(self, guid: str, classifications: list[dict]) -> dict:
        """POST /v2/entity/guid/{guid}/classifications"""
        return await self._request(
            "POST", f"/entity/guid/{_safe(guid)}/classifications", json_body=classifications
        )

    async def remove_classification(self, guid: str, classification_name: str) -> dict:
        """DELETE /v2/entity/guid/{guid}/classification/{classificationName}"""
        return await self._request(
            "DELETE",
            f"/entity/guid/{_safe(guid)}/classification/{_safe(classification_name)}",
        )

    # * Glossary endpoints

    async def get_glossaries(self, limit: int = 25, offset: int = 0, sort: str = "ASC") -> list:
        """GET /v2/glossary"""
        params = {"limit": limit, "offset": offset, "sort": sort}
        return await self._request("GET", "/glossary", params=params)

    async def get_glossary(self, glossary_guid: str) -> dict:
        """GET /v2/glossary/{glossaryGuid}"""
        return await self._request("GET", f"/glossary/{_safe(glossary_guid)}")

    async def get_glossary_terms(
        self, glossary_guid: str, limit: int = 25, offset: int = 0, sort: str = "ASC"
    ) -> list:
        """GET /v2/glossary/{glossaryGuid}/terms"""
        params = {"limit": limit, "offset": offset, "sort": sort}
        return await self._request("GET", f"/glossary/{_safe(glossary_guid)}/terms", params=params)

    async def get_glossary_term(self, term_guid: str) -> dict:
        """GET /v2/glossary/term/{termGuid}"""
        return await self._request("GET", f"/glossary/term/{_safe(term_guid)}")

    # * Type definition endpoints

    async def get_all_type_defs(self) -> dict:
        """GET /v2/types/typedefs"""
        return await self._request("GET", "/types/typedefs")

    async def get_type_def_by_name(self, name: str) -> dict:
        """GET /v2/types/typedef/name/{name}"""
        return await self._request("GET", f"/types/typedef/name/{_safe(name)}")

    async def get_type_def_by_guid(self, guid: str) -> dict:
        """GET /v2/types/typedef/guid/{guid}"""
        return await self._request("GET", f"/types/typedef/guid/{_safe(guid)}")

    async def get_entity_def_by_name(self, name: str) -> dict:
        """GET /v2/types/entitydef/name/{name}"""
        return await self._request("GET", f"/types/entitydef/name/{_safe(name)}")

    async def get_classification_def_by_name(self, name: str) -> dict:
        """GET /v2/types/classificationdef/name/{name}"""
        return await self._request("GET", f"/types/classificationdef/name/{_safe(name)}")
