"""Classification (tag) management tools for Apache Atlas."""

from fastmcp import Context

from apache_atlas_mcp.tools.helpers import get_client


async def get_classifications(ctx: Context, guid: str) -> dict:
    """Get all classifications (tags) applied to an entity.

    Classifications are used for data governance — e.g., PII,
    Confidential, HIPAA, GDPR tags that indicate sensitivity
    or compliance requirements.

    Args:
        guid: The GUID of the entity.
    """
    client = get_client(ctx)
    return await client.get_classifications(guid=guid)


async def add_classification(
    ctx: Context,
    guid: str,
    classification_name: str,
    attributes: dict | None = None,
    propagate: bool = True,
) -> dict:
    """Add a classification (tag) to an entity.

    Classifications propagate through lineage by default — e.g.,
    marking a source table as PII will automatically tag downstream
    tables and columns.

    Args:
        guid: The GUID of the entity to classify.
        classification_name: Name of the classification (e.g., "PII", "Confidential").
        attributes: Optional classification attributes.
        propagate: Whether to propagate through lineage (default: true).
    """
    client = get_client(ctx)
    classification = {
        "typeName": classification_name,
        "propagate": propagate,
    }
    if attributes:
        classification["attributes"] = attributes
    return await client.add_classifications(guid=guid, classifications=[classification])


async def remove_classification(ctx: Context, guid: str, classification_name: str) -> dict:
    """Remove a classification (tag) from an entity.

    Args:
        guid: The GUID of the entity.
        classification_name: Name of the classification to remove.
    """
    client = get_client(ctx)
    return await client.remove_classification(guid=guid, classification_name=classification_name)
