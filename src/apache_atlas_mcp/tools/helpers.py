"""Shared helpers for tool modules."""

from urllib.parse import quote

from fastmcp import Context

from apache_atlas_mcp.client import AtlasClient


def get_client(ctx: Context) -> AtlasClient:
    """Extract the Atlas client from the request context."""
    return ctx.lifespan_context["atlas_client"]


def safe_path(segment: str) -> str:
    """URL-encode a path segment to prevent path traversal."""
    return quote(segment, safe="")
