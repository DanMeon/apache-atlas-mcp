"""Entity CRUD and search tools for Apache Atlas."""

from fastmcp import Context

from apache_atlas_mcp.tools.helpers import get_client


async def search_entities(
    ctx: Context,
    query: str | None = None,
    type_name: str | None = None,
    classification: str | None = None,
    limit: int = 25,
    offset: int = 0,
) -> dict:
    """Search for entities in Apache Atlas using basic search.

    Finds data assets (tables, columns, processes, etc.) by keyword,
    type, or classification. Returns matching entity headers with
    key attributes.

    Args:
        query: Free-text search query (e.g., "customer_orders").
        type_name: Filter by entity type (e.g., "hive_table", "rdbms_table").
        classification: Filter by classification tag (e.g., "PII", "Confidential").
        limit: Maximum number of results (default: 25, max: 100).
        offset: Pagination offset.
    """
    client = get_client(ctx)
    return await client.basic_search(
        query=query,
        type_name=type_name,
        classification=classification,
        limit=min(limit, 100),
        offset=offset,
    )


async def dsl_search(ctx: Context, query: str, limit: int = 25, offset: int = 0) -> dict:
    """Execute an Atlas DSL (Domain Specific Language) search query.

    Atlas DSL supports structured queries with type filters, attribute
    conditions, and aggregations. Useful for complex, precise queries.

    Example DSL queries:
    - "hive_table where name = 'customers'"
    - "hive_column where table.name = 'orders'"
    - "DataSet where owner = 'analytics_team'"

    Args:
        query: Atlas DSL query string.
        limit: Maximum number of results (default: 25).
        offset: Pagination offset.
    """
    client = get_client(ctx)
    return await client.dsl_search(query=query, limit=min(limit, 100), offset=offset)


async def quick_search(
    ctx: Context, query: str, type_name: str | None = None, limit: int = 25
) -> dict:
    """Perform a quick search across all entity types.

    Faster than basic search, optimized for autocomplete-style lookups.
    Good for finding entities when you have a partial name.

    Args:
        query: Search text (supports partial matching).
        type_name: Optional type filter (e.g., "hive_table").
        limit: Maximum number of results (default: 25).
    """
    client = get_client(ctx)
    return await client.quick_search(query=query, type_name=type_name, limit=min(limit, 100))


async def get_entity(
    ctx: Context,
    guid: str,
    min_ext_info: bool = False,
    ignore_relationships: bool = False,
) -> dict:
    """Get full details of an entity by its GUID.

    Returns the complete entity with all attributes, classifications,
    relationship attributes, and optionally referred entities.

    Args:
        guid: The unique identifier (GUID) of the entity.
        min_ext_info: If true, returns minimal info for referred entities.
        ignore_relationships: If true, omits relationship attributes.
    """
    client = get_client(ctx)
    return await client.get_entity_by_guid(
        guid=guid, min_ext_info=min_ext_info, ignore_relationships=ignore_relationships
    )


async def get_entity_by_attribute(
    ctx: Context, type_name: str, attribute_name: str, attribute_value: str
) -> dict:
    """Get an entity by its unique attribute value.

    Useful when you know the qualified name or another unique attribute
    instead of the GUID. Common pattern: look up by qualifiedName.

    Args:
        type_name: The entity type (e.g., "hive_table", "rdbms_table").
        attribute_name: Unique attribute name (typically "qualifiedName").
        attribute_value: The attribute value to match.
    """
    client = get_client(ctx)
    return await client.get_entity_by_unique_attribute(
        type_name=type_name, attr_name=attribute_name, attr_value=attribute_value
    )


async def get_entities_bulk(ctx: Context, guids: list[str]) -> dict:
    """Get multiple entities by their GUIDs in a single request.

    Efficient way to fetch details for several entities at once,
    e.g., after collecting GUIDs from a search or lineage query.

    Args:
        guids: List of entity GUIDs to retrieve (max 25).
    """
    client = get_client(ctx)
    return await client.get_entities_by_guids(guids=guids[:25])


async def create_entity(ctx: Context, entity: dict) -> dict:
    """Create or update an entity in Atlas.

    The entity dict must include at minimum:
    - typeName: The entity type (e.g., "hive_table")
    - attributes: Dict of attribute values (must include "qualifiedName" and "name")

    If an entity with the same qualifiedName exists, it will be updated.

    Args:
        entity: Entity definition dict with typeName and attributes.
    """
    if "typeName" not in entity:
        raise ValueError("entity must include 'typeName'")
    if "attributes" not in entity:
        raise ValueError("entity must include 'attributes'")
    client = get_client(ctx)
    return await client.create_or_update_entity(entity=entity)


async def delete_entity(ctx: Context, guid: str) -> dict:
    """Soft-delete an entity by its GUID.

    The entity is marked as DELETED but remains in the system.
    This is a non-destructive operation — the entity can still
    be found via search with includeDeleted=true.

    Args:
        guid: The unique identifier (GUID) of the entity to delete.
    """
    client = get_client(ctx)
    return await client.delete_entity_by_guid(guid=guid)
