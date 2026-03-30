"""Tests for server module — tool registration and read-only mode."""


class TestReadOnlyMode:
    def test_default_is_read_only(self, monkeypatch):
        monkeypatch.setenv("ATLAS_USERNAME", "u")
        monkeypatch.setenv("ATLAS_PASSWORD", "p")
        monkeypatch.delenv("ATLAS_ALLOW_WRITE", raising=False)

        from importlib import reload

        import apache_atlas_mcp.server as server_mod

        reload(server_mod)
        assert server_mod._allow_write is False

    def test_write_mode_via_env(self, monkeypatch):
        monkeypatch.setenv("ATLAS_USERNAME", "u")
        monkeypatch.setenv("ATLAS_PASSWORD", "p")
        monkeypatch.setenv("ATLAS_ALLOW_WRITE", "true")

        from importlib import reload

        import apache_atlas_mcp.server as server_mod

        reload(server_mod)
        assert server_mod._allow_write is True


class TestModels:
    def test_pydantic_models_import(self):
        from apache_atlas_mcp.models import (
            AtlasLineageInfo,
            AtlasSearchResult,
        )

        assert AtlasSearchResult is not None
        assert AtlasLineageInfo is not None

    def test_populate_by_name(self):
        from apache_atlas_mcp.models import AtlasSearchResult

        result = AtlasSearchResult(query_type="BASIC", type_name="hive_table")
        assert result.query_type == "BASIC"
        assert result.type_name == "hive_table"

    def test_populate_by_alias(self):
        from apache_atlas_mcp.models import AtlasSearchResult

        result = AtlasSearchResult(**{"queryType": "DSL", "typeName": "JadxDataset"})
        assert result.query_type == "DSL"
        assert result.type_name == "JadxDataset"
