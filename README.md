<p align="center">
  <img src="https://raw.githubusercontent.com/DanMeon/apache-atlas-mcp/main/assets/banner.svg" alt="Apache Atlas MCP Server" width="900" />
</p>

<p align="center">
  <a href="https://github.com/DanMeon/apache-atlas-mcp/actions/workflows/ci.yml"><img src="https://github.com/DanMeon/apache-atlas-mcp/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+" /></a>
</p>

A community-built [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that connects LLM agents to [Apache Atlas](https://atlas.apache.org/) metadata governance platform. Not affiliated with the Apache Software Foundation.

**Read-only by default.** Write operations (create/delete entities, manage classifications) require explicit opt-in via `--write` flag or `ATLAS_ALLOW_WRITE=true`.

## Why?

Apache Atlas is a widely-used open-source metadata governance framework for Hadoop ecosystems and beyond. With the 2.4.0 release (Jan 2025) breaking a 2-year gap and 2.5.0 (RC) adding PostgreSQL backend support and Trino extractor, Atlas is seeing renewed activity.

This MCP server lets AI agents:
- **Search** data assets across your entire metadata catalog
- **Trace lineage** — understand how data flows from source to destination
- **Browse glossaries** — look up business terms and definitions
- **Inspect types** — understand the metadata schema structure
- **Manage classifications** — apply governance tags like PII, GDPR, Confidential *(write mode)*
- **Create/delete entities** — modify metadata catalog *(write mode)*

<p align="center">
  <img src="https://raw.githubusercontent.com/DanMeon/apache-atlas-mcp/main/assets/search-demo.png" alt="Search entities demo" width="800" />
</p>

## Quick Start

### Installation

```bash
# Using uv (recommended)
uv add apache-atlas-mcp

# Using pip
pip install apache-atlas-mcp

# Run without installing
uvx apache-atlas-mcp
```

### Configuration

Set environment variables to connect to your Atlas instance:

```bash
export ATLAS_BASE_URL=http://localhost:21000
export ATLAS_USERNAME=your-username
export ATLAS_PASSWORD=your-password
```

All configuration options:

| Variable | Default | Description |
|---|---|---|
| `ATLAS_BASE_URL` | `http://localhost:21000` | Atlas server URL |
| `ATLAS_USERNAME` | *(required)* | Authentication username |
| `ATLAS_PASSWORD` | *(required)* | Authentication password |
| `ATLAS_VERIFY_SSL` | `true` | Verify SSL certificates |
| `ATLAS_TIMEOUT` | `30` | HTTP request timeout (seconds) |
| `ATLAS_ALLOW_WRITE` | `false` | Enable write operations (create, delete, classify) |

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apache-atlas": {
      "command": "uvx",
      "args": ["apache-atlas-mcp"],
      "env": {
        "ATLAS_BASE_URL": "http://localhost:21000",
        "ATLAS_USERNAME": "admin",
        "ATLAS_PASSWORD": "your-password"
      }
    }
  }
}
```

To enable write operations:

```json
{
  "mcpServers": {
    "apache-atlas": {
      "command": "uvx",
      "args": ["apache-atlas-mcp", "--write"],
      "env": {
        "ATLAS_BASE_URL": "http://localhost:21000",
        "ATLAS_USERNAME": "admin",
        "ATLAS_PASSWORD": "your-password"
      }
    }
  }
}
```

### Usage with Claude Code

```bash
# Read-only (default)
claude mcp add atlas-server -- uvx apache-atlas-mcp

# With write operations enabled
claude mcp add atlas-server -- uvx apache-atlas-mcp --write
```

### Run Directly

```bash
# Read-only (default)
apache-atlas-mcp

# With write operations enabled
apache-atlas-mcp --write
```

## Available Tools

### Read-Only Tools (always available)

#### Entity Search

| Tool | Description |
|---|---|
| `search_entities` | Basic search by keyword, type, or classification |
| `dsl_search` | Advanced search using Atlas DSL query language |
| `quick_search` | Fast partial-match search (autocomplete-style) |
| `get_entity` | Get full entity details by GUID |
| `get_entity_by_attribute` | Get entity by unique attribute (e.g., qualifiedName) |
| `get_entities_bulk` | Fetch multiple entities by GUIDs |

#### Lineage

| Tool | Description |
|---|---|
| `get_lineage` | Trace upstream/downstream data flow by GUID |
| `get_lineage_by_attribute` | Trace lineage by unique attribute |

#### Classifications

| Tool | Description |
|---|---|
| `get_classifications` | List all classifications on an entity |

#### Glossary

| Tool | Description |
|---|---|
| `list_glossaries` | List all business glossaries |
| `get_glossary` | Get glossary details with terms and categories |
| `get_glossary_terms` | List terms in a glossary |
| `get_glossary_term` | Get full details of a glossary term |

#### Type Definitions

| Tool | Description |
|---|---|
| `get_all_type_definitions` | Get the complete Atlas type system |
| `get_type_definition` | Get a specific type definition by name |
| `get_entity_type_definition` | Get an entity type with all attributes |

### Write Tools (requires `--write` or `ATLAS_ALLOW_WRITE=true`)

| Tool | Description |
|---|---|
| `create_entity` | Create or update an entity |
| `delete_entity` | Soft-delete an entity |
| `add_classification` | Apply a classification tag (with lineage propagation) |
| `remove_classification` | Remove a classification from an entity |

## Architecture

```
LLM Agent  <-->  MCP Protocol  <-->  Apache Atlas MCP Server  <-->  Atlas REST API v2
                                              |
                                       FastMCP + httpx
                                              |
                                     Apache Atlas Instance
                                     (HBase / PostgreSQL backend)
```

The server wraps the [Atlas REST API v2](https://atlas.apache.org/api/v2/index.html) using:
- **[FastMCP](https://github.com/PrefectHQ/fastmcp)** for MCP protocol handling
- **[httpx](https://www.python-httpx.org/)** for async HTTP communication
- **[Pydantic V2](https://docs.pydantic.dev/)** for data validation and serialization

The REST API is backend-independent — it works regardless of whether Atlas uses HBase, Cassandra, or the new PostgreSQL backend (Atlas 2.5.0+).

## Compatibility

- **Apache Atlas**: 2.1.0+ (tested with 2.3.2 and 2.4.0)
- **Python**: 3.11+
- **Authentication**: HTTP Basic (Atlas file-based auth, LDAP, or AD — all use Basic HTTP headers)

## Development

```bash
# Clone the repository
git clone https://github.com/DanMeon/apache-atlas-mcp.git
cd apache-atlas-mcp

# Install dependencies
uv sync --group dev

# Run tests
uv run pytest tests/ -v --cov

# Lint & type check
uv run ruff check src/ tests/
uv run pyright src/apache_atlas_mcp/
```

## License

MIT
