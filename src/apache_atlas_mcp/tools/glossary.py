"""Glossary browsing tools for Apache Atlas."""

from fastmcp import Context

from apache_atlas_mcp.tools.helpers import get_client


async def list_glossaries(ctx: Context, limit: int = 25, offset: int = 0) -> list:
    """List all business glossaries.

    Glossaries organize business terms and definitions, providing
    a shared vocabulary for data assets across the organization.

    Args:
        limit: Maximum number of glossaries to return.
        offset: Pagination offset.
    """
    client = get_client(ctx)
    return await client.get_glossaries(limit=limit, offset=offset)


async def get_glossary(ctx: Context, glossary_guid: str) -> dict:
    """Get a glossary by its GUID, including its terms and categories.

    Args:
        glossary_guid: The GUID of the glossary.
    """
    client = get_client(ctx)
    return await client.get_glossary(glossary_guid=glossary_guid)


async def get_glossary_terms(
    ctx: Context, glossary_guid: str, limit: int = 25, offset: int = 0
) -> list:
    """List terms in a specific glossary.

    Returns business terms with their definitions, linked entities,
    and category assignments.

    Args:
        glossary_guid: The GUID of the glossary.
        limit: Maximum number of terms to return.
        offset: Pagination offset.
    """
    client = get_client(ctx)
    return await client.get_glossary_terms(
        glossary_guid=glossary_guid, limit=limit, offset=offset
    )


async def get_glossary_term(ctx: Context, term_guid: str) -> dict:
    """Get a glossary term by its GUID.

    Returns the full term including definition, linked entities,
    related terms (seeAlso), and category assignments.

    Args:
        term_guid: The GUID of the glossary term.
    """
    client = get_client(ctx)
    return await client.get_glossary_term(term_guid=term_guid)
