"""Tests for the Atlas REST API client."""

import httpx
import pytest

from apache_atlas_mcp.client import AtlasClient, _safe
from tests.conftest import (
    SAMPLE_CLASSIFICATIONS,
    SAMPLE_ENTITY,
    SAMPLE_LINEAGE,
    SAMPLE_SEARCH_RESULT,
)

# * URL encoding


class TestSafePath:
    def test_normal_string(self):
        assert _safe("abc-123") == "abc-123"

    def test_path_traversal(self):
        assert _safe("../../admin") == "..%2F..%2Fadmin"

    def test_special_characters(self):
        assert _safe("name with spaces") == "name%20with%20spaces"

    def test_slashes(self):
        assert _safe("a/b/c") == "a%2Fb%2Fc"


# * HTTP request handling


class TestClientRequest:
    @pytest.mark.asyncio
    async def test_get_entity_by_guid(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/entity/guid/abc-123-def").mock(
            return_value=httpx.Response(200, json=SAMPLE_ENTITY)
        )
        result = await atlas_client.get_entity_by_guid("abc-123-def")
        assert result["entity"]["guid"] == "abc-123-def"
        assert result["entity"]["typeName"] == "JadxDataset"
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_basic_search(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/search/basic").mock(
            return_value=httpx.Response(200, json=SAMPLE_SEARCH_RESULT)
        )
        result = await atlas_client.basic_search(query="*", type_name="JadxDataset")
        assert result["queryType"] == "BASIC"
        assert len(result["entities"]) == 1
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_dsl_search(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/search/dsl").mock(
            return_value=httpx.Response(200, json=SAMPLE_SEARCH_RESULT)
        )
        result = await atlas_client.dsl_search(query="JadxDataset")
        assert result["queryType"] == "BASIC"
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_get_lineage(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/lineage/abc-123-def").mock(
            return_value=httpx.Response(200, json=SAMPLE_LINEAGE)
        )
        result = await atlas_client.get_lineage("abc-123-def")
        assert result["baseEntityGuid"] == "abc-123-def"
        assert len(result["relations"]) == 1
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_get_classifications(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/entity/guid/abc-123-def/classifications").mock(
            return_value=httpx.Response(200, json=SAMPLE_CLASSIFICATIONS)
        )
        result = await atlas_client.get_classifications("abc-123-def")
        assert result["list"][0]["typeName"] == "PII"
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_delete_entity(self, atlas_client: AtlasClient, mock_api):
        mock_api.delete("/entity/guid/abc-123-def").mock(return_value=httpx.Response(204))
        result = await atlas_client.delete_entity_by_guid("abc-123-def")
        assert result == {}
        await atlas_client.close()


# * Error handling


class TestClientErrors:
    @pytest.mark.asyncio
    async def test_401_raises_auth_error(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/entity/guid/abc").mock(return_value=httpx.Response(401, text="Unauthorized"))
        with pytest.raises(ValueError, match="authentication failed"):
            await atlas_client.get_entity_by_guid("abc")
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_403_raises_access_denied(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/entity/guid/abc").mock(return_value=httpx.Response(403, text="Forbidden"))
        with pytest.raises(ValueError, match="Access denied"):
            await atlas_client.get_entity_by_guid("abc")
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_404_raises_not_found(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/entity/guid/nonexistent").mock(
            return_value=httpx.Response(404, text="Not Found")
        )
        with pytest.raises(ValueError, match="not found"):
            await atlas_client.get_entity_by_guid("nonexistent")
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_500_raises_api_error(self, atlas_client: AtlasClient, mock_api):
        mock_api.get("/search/basic").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        with pytest.raises(ValueError, match="Atlas API error"):
            await atlas_client.basic_search(query="*")
        await atlas_client.close()


# * URL encoding in requests


class TestClientUrlEncoding:
    @pytest.mark.asyncio
    async def test_guid_with_special_chars(self, atlas_client: AtlasClient, mock_api):
        # ^ _safe() encodes "../" to "%2F", respx matches decoded path
        mock_api.get(url__regex=r"/entity/guid/abc%2F\.\.%2Fdef").mock(
            return_value=httpx.Response(200, json=SAMPLE_ENTITY)
        )
        result = await atlas_client.get_entity_by_guid("abc/../def")
        assert result["entity"]["guid"] == "abc-123-def"
        await atlas_client.close()

    @pytest.mark.asyncio
    async def test_type_name_encoded(self, atlas_client: AtlasClient, mock_api):
        mock_api.get(url__regex=r"/types/entitydef/name/my%20type").mock(
            return_value=httpx.Response(200, json={"name": "my type"})
        )
        result = await atlas_client.get_entity_def_by_name("my type")
        assert result["name"] == "my type"
        await atlas_client.close()
