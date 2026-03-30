"""Shared test fixtures for Apache Atlas MCP server tests."""

import pytest
import respx

from apache_atlas_mcp.client import AtlasClient
from apache_atlas_mcp.config import AtlasSettings

ATLAS_BASE = "http://atlas-test:21000/api/atlas/v2"


@pytest.fixture
def settings() -> AtlasSettings:
    return AtlasSettings(
        base_url="http://atlas-test:21000",
        username="testuser",
        password="testpass",
    )


@pytest.fixture
def atlas_client(settings: AtlasSettings) -> AtlasClient:
    return AtlasClient(settings)


@pytest.fixture
def mock_api():
    """Activate respx mock for all httpx requests."""
    with respx.mock(base_url=ATLAS_BASE) as api:
        yield api


# * Sample response data


SAMPLE_ENTITY_HEADER = {
    "typeName": "JadxDataset",
    "guid": "abc-123-def",
    "status": "ACTIVE",
    "displayText": "Test Dataset",
    "attributes": {
        "qualifiedName": "test_dataset",
        "name": "Test Dataset",
        "description": "A test dataset",
    },
    "classificationNames": ["PII"],
    "meaningNames": [],
    "meanings": [],
    "isIncomplete": False,
    "labels": [],
}

SAMPLE_ENTITY = {
    "entity": {
        "typeName": "JadxDataset",
        "guid": "abc-123-def",
        "status": "ACTIVE",
        "attributes": {
            "qualifiedName": "test_dataset",
            "name": "Test Dataset",
            "owner": "admin",
        },
        "classifications": [],
    },
    "referredEntities": {},
}

SAMPLE_SEARCH_RESULT = {
    "queryType": "BASIC",
    "searchParameters": {"query": "*", "limit": 25, "offset": 0},
    "entities": [SAMPLE_ENTITY_HEADER],
    "approximateCount": 1,
}

SAMPLE_LINEAGE = {
    "baseEntityGuid": "abc-123-def",
    "lineageDirection": "BOTH",
    "lineageDepth": 3,
    "guidEntityMap": {
        "abc-123-def": SAMPLE_ENTITY_HEADER,
        "xyz-789-uvw": {
            "typeName": "JadxDataset",
            "guid": "xyz-789-uvw",
            "status": "ACTIVE",
            "displayText": "Source Dataset",
        },
    },
    "relations": [
        {
            "fromEntityId": "xyz-789-uvw",
            "toEntityId": "abc-123-def",
            "relationshipId": "rel-001",
        }
    ],
}

SAMPLE_GLOSSARY = {
    "guid": "glossary-001",
    "qualifiedName": "test_glossary",
    "name": "Test Glossary",
    "shortDescription": "A test glossary",
}

SAMPLE_GLOSSARY_TERM = {
    "guid": "term-001",
    "qualifiedName": "test_term",
    "name": "Test Term",
    "shortDescription": "A test term",
    "anchor": {"glossaryGuid": "glossary-001", "displayText": "Test Glossary"},
}

SAMPLE_TYPE_DEF = {
    "category": "ENTITY",
    "name": "JadxDataset",
    "description": "Custom dataset type",
    "attributeDefs": [
        {"name": "qualifiedName", "typeName": "string", "isOptional": False},
        {"name": "name", "typeName": "string", "isOptional": False},
    ],
    "superTypes": ["DataSet"],
}

SAMPLE_CLASSIFICATIONS = {
    "list": [{"typeName": "PII", "entityGuid": "abc-123-def", "propagate": True}],
}
