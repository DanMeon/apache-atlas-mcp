"""Apache Atlas MCP Server.

Exposes Apache Atlas metadata governance capabilities as MCP tools,
enabling LLM agents to search entities, trace lineage, manage
classifications, browse glossaries, and inspect type definitions.

By default, only read-only tools are registered. Pass --write or
set ATLAS_ALLOW_WRITE=true to enable write operations (create, update,
delete entities and manage classifications).
"""

import os
import sys

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apache_atlas_mcp.client import AtlasClient
from apache_atlas_mcp.config import AtlasSettings
from apache_atlas_mcp.tools.classification import (
    add_classification,
    get_classifications,
    remove_classification,
)
from apache_atlas_mcp.tools.entity import (
    create_entity,
    delete_entity,
    dsl_search,
    get_entities_bulk,
    get_entity,
    get_entity_by_attribute,
    quick_search,
    search_entities,
)
from apache_atlas_mcp.tools.glossary import (
    get_glossary,
    get_glossary_term,
    get_glossary_terms,
    list_glossaries,
)
from apache_atlas_mcp.tools.lineage import get_lineage, get_lineage_by_attribute
from apache_atlas_mcp.tools.typedefs import (
    get_all_type_definitions,
    get_entity_type_definition,
    get_type_definition,
)


def _resolve_write_mode() -> bool:
    """Determine write mode from CLI flag or environment variable.

    --write flag takes precedence, then falls back to ATLAS_ALLOW_WRITE env var.
    """
    if "--write" in sys.argv:
        sys.argv.remove("--write")
        return True
    return os.environ.get("ATLAS_ALLOW_WRITE", "false").lower() in ("true", "1", "yes")


_allow_write = _resolve_write_mode()
_settings = AtlasSettings(allow_write=_allow_write)  # pyright: ignore[reportCallIssue]


@lifespan
async def app_lifespan(server):
    """Manage the Atlas HTTP client lifecycle."""
    client = AtlasClient(_settings)
    try:
        yield {"atlas_client": client}
    finally:
        await client.close()


def _build_instructions() -> str:
    base = (
        "This server connects to Apache Atlas for metadata governance. "
        "Use it to search data assets, trace data lineage, "
        "browse business glossaries, and inspect type definitions. "
        "All operations require a running Apache Atlas instance."
    )
    if _allow_write:
        return base + (
            " Write operations are ENABLED — you can create/update/delete entities "
            "and manage classifications. Use write tools with caution."
        )
    return base + " This server is running in READ-ONLY mode."


mcp = FastMCP(
    name="Apache Atlas MCP Server",
    instructions=_build_instructions(),
    lifespan=app_lifespan,
)

# * Read-only tools (always registered)

# * Entity read tools
mcp.tool(search_entities)
mcp.tool(dsl_search)
mcp.tool(quick_search)
mcp.tool(get_entity)
mcp.tool(get_entity_by_attribute)
mcp.tool(get_entities_bulk)

# * Lineage tools
mcp.tool(get_lineage)
mcp.tool(get_lineage_by_attribute)

# * Classification read tools
mcp.tool(get_classifications)

# * Glossary tools
mcp.tool(list_glossaries)
mcp.tool(get_glossary)
mcp.tool(get_glossary_terms)
mcp.tool(get_glossary_term)

# * Type definition tools
mcp.tool(get_all_type_definitions)
mcp.tool(get_type_definition)
mcp.tool(get_entity_type_definition)

# * Write tools (only when --write flag or ATLAS_ALLOW_WRITE=true)

if _allow_write:
    mcp.tool(create_entity)
    mcp.tool(delete_entity)
    mcp.tool(add_classification)
    mcp.tool(remove_classification)


def main() -> None:
    """Entry point for the Apache Atlas MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
