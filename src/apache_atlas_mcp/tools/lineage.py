"""Lineage tracing tools for Apache Atlas."""

from typing import Literal

from fastmcp import Context

from apache_atlas_mcp.tools.helpers import get_client

LineageDirection = Literal["INPUT", "OUTPUT", "BOTH"]


async def get_lineage(
    ctx: Context, guid: str, direction: LineageDirection = "BOTH", depth: int = 3
) -> dict:
    """Get the data lineage graph for an entity.

    Traces upstream (INPUT) and/or downstream (OUTPUT) data flow
    relationships. This is the most valuable tool for understanding
    how data moves through your system.

    The response includes:
    - guidEntityMap: All entities in the lineage graph
    - relations: Directed edges showing data flow

    Args:
        guid: The GUID of the entity to trace lineage for.
        direction: "INPUT" (upstream), "OUTPUT" (downstream), or "BOTH".
        depth: How many hops to traverse (default: 3, max: 10).
    """
    client = get_client(ctx)
    return await client.get_lineage(
        guid=guid, direction=direction, depth=min(depth, 10)
    )


async def get_lineage_by_attribute(
    ctx: Context,
    type_name: str,
    attribute_name: str,
    attribute_value: str,
    direction: LineageDirection = "BOTH",
    depth: int = 3,
) -> dict:
    """Get lineage for an entity identified by a unique attribute.

    Same as get_lineage but uses a unique attribute (like qualifiedName)
    instead of a GUID. Convenient when you know the entity's name
    but not its GUID.

    Args:
        type_name: Entity type (e.g., "hive_table").
        attribute_name: Unique attribute name (typically "qualifiedName").
        attribute_value: The attribute value to match.
        direction: "INPUT" (upstream), "OUTPUT" (downstream), or "BOTH".
        depth: How many hops to traverse (default: 3, max: 10).
    """
    client = get_client(ctx)
    return await client.get_lineage_by_unique_attribute(
        type_name=type_name,
        attr_name=attribute_name,
        attr_value=attribute_value,
        direction=direction,
        depth=min(depth, 10),
    )
