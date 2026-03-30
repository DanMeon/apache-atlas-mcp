# Apache Atlas MCP Server

# Run MCP Inspector (dev mode)
dev:
    uv run fastmcp dev inspector src/apache_atlas_mcp/server.py:mcp

# Run server (read-only)
run:
    uv run apache-atlas-mcp

# Run server with write mode
run-write:
    uv run apache-atlas-mcp --write

# Install dependencies
install:
    uv sync --group dev

# Run tests with coverage
test:
    uv run pytest -v --cov --cov-report=term-missing

# Lint
lint:
    uv run ruff check src/ tests/

# Format
fmt:
    uv run ruff format src/ tests/

# Type check
typecheck:
    uv run pyright src/apache_atlas_mcp/

# All checks (lint + typecheck + test)
check: lint typecheck test
