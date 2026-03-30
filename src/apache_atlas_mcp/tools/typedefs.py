"""Type definition inspection tools for Apache Atlas."""

from fastmcp import Context

from apache_atlas_mcp.tools.helpers import get_client


async def get_all_type_definitions(ctx: Context) -> dict:
    """Get all type definitions from Atlas.

    Returns the complete type system including entity types,
    classification types, relationship types, enum types, and
    struct types. This is useful for understanding the metadata
    schema structure.

    Warning: This can return a large response. Consider using
    get_type_definition for specific types instead.
    """
    client = get_client(ctx)
    return await client.get_all_type_defs()


async def get_type_definition(ctx: Context, name: str) -> dict:
    """Get a specific type definition by name.

    Returns the full type definition including attributes,
    super types, and constraints. Useful for understanding
    what attributes an entity type has.

    Args:
        name: The type name (e.g., "hive_table", "rdbms_column", "PII").
    """
    client = get_client(ctx)
    return await client.get_type_def_by_name(name=name)


async def get_entity_type_definition(ctx: Context, name: str) -> dict:
    """Get an entity type definition by name.

    Returns the entity type definition with all attribute definitions,
    super types, sub types, and relationship attribute definitions.

    Args:
        name: The entity type name (e.g., "hive_table", "hive_db", "rdbms_table").
    """
    client = get_client(ctx)
    return await client.get_entity_def_by_name(name=name)
