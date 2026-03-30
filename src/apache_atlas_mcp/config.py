from pydantic_settings import BaseSettings


class AtlasSettings(BaseSettings):
    """Configuration for Apache Atlas MCP server.

    All settings can be configured via environment variables
    with the ATLAS_ prefix (e.g., ATLAS_BASE_URL).
    """

    model_config = {"env_prefix": "ATLAS_", "env_file": ".env", "env_file_encoding": "utf-8"}

    base_url: str
    username: str
    password: str
    verify_ssl: bool = True
    timeout: int = 30
    allow_write: bool = False
