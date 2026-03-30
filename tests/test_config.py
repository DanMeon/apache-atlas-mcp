"""Tests for configuration module."""

import pytest

from apache_atlas_mcp.config import AtlasSettings


class TestAtlasSettings:
    def test_defaults(self, monkeypatch):
        monkeypatch.delenv("ATLAS_BASE_URL", raising=False)
        monkeypatch.delenv("ATLAS_VERIFY_SSL", raising=False)
        monkeypatch.delenv("ATLAS_TIMEOUT", raising=False)
        monkeypatch.delenv("ATLAS_ALLOW_WRITE", raising=False)
        settings = AtlasSettings(username="u", password="p", _env_file=None)
        assert settings.base_url == "http://localhost:21000"
        assert settings.verify_ssl is True
        assert settings.timeout == 30
        assert settings.allow_write is False

    def test_custom_values(self):
        settings = AtlasSettings(
            base_url="http://custom:9999",
            username="admin",
            password="secret",
            verify_ssl=False,
            timeout=60,
            allow_write=True,
            _env_file=None,
        )
        assert settings.base_url == "http://custom:9999"
        assert settings.verify_ssl is False
        assert settings.timeout == 60
        assert settings.allow_write is True

    def test_requires_username(self, monkeypatch):
        monkeypatch.delenv("ATLAS_USERNAME", raising=False)
        monkeypatch.delenv("ATLAS_PASSWORD", raising=False)
        with pytest.raises(Exception):
            AtlasSettings(password="p", _env_file=None)

    def test_requires_password(self, monkeypatch):
        monkeypatch.delenv("ATLAS_USERNAME", raising=False)
        monkeypatch.delenv("ATLAS_PASSWORD", raising=False)
        with pytest.raises(Exception):
            AtlasSettings(username="u", _env_file=None)

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("ATLAS_BASE_URL", "http://env-host:21000")
        monkeypatch.setenv("ATLAS_USERNAME", "env-user")
        monkeypatch.setenv("ATLAS_PASSWORD", "env-pass")
        monkeypatch.setenv("ATLAS_ALLOW_WRITE", "true")
        settings = AtlasSettings(_env_file=None)
        assert settings.base_url == "http://env-host:21000"
        assert settings.username == "env-user"
        assert settings.password == "env-pass"
        assert settings.allow_write is True
