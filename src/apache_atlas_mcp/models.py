"""Pydantic V2 models for Apache Atlas REST API v2 responses.

These models represent the core data structures returned by the Atlas API.
Fields use `None` defaults for optional attributes since Atlas responses
vary based on entity type and query parameters.

Note: These models are available for consumers of this package who want
typed responses. The MCP tools return raw dicts for simplicity, but
callers can validate responses with e.g. AtlasSearchResult(**raw_dict).
"""

from pydantic import BaseModel, ConfigDict, Field


class _AtlasBase(BaseModel):
    """Shared config for all Atlas models."""

    model_config = ConfigDict(populate_by_name=True)


# * Entity Models


class AtlasClassification(_AtlasBase):
    """A classification (tag) applied to an entity."""

    type_name: str = Field(alias="typeName")
    entity_guid: str | None = Field(default=None, alias="entityGuid")
    propagate: bool | None = None
    attributes: dict | None = None
    validity_periods: list[dict] | None = Field(default=None, alias="validityPeriods")


class AtlasEntityHeader(_AtlasBase):
    """Lightweight entity representation used in search results and lineage."""

    type_name: str = Field(alias="typeName")
    guid: str
    status: str | None = None
    display_text: str | None = Field(default=None, alias="displayText")
    attributes: dict | None = None
    classification_names: list[str] | None = Field(default=None, alias="classificationNames")
    classifications: list[AtlasClassification] | None = None
    meaning_names: list[str] | None = Field(default=None, alias="meaningNames")
    meanings: list[dict] | None = None
    is_incomplete: bool | None = Field(default=None, alias="isIncomplete")
    labels: list[str] | None = None


class AtlasEntity(_AtlasBase):
    """Full entity representation with all attributes and relationships."""

    type_name: str = Field(alias="typeName")
    guid: str | None = None
    status: str | None = None
    display_text: str | None = Field(default=None, alias="displayText")
    attributes: dict | None = None
    relationship_attributes: dict | None = Field(default=None, alias="relationshipAttributes")
    classifications: list[AtlasClassification] | None = None
    meanings: list[dict] | None = None
    labels: list[str] | None = None
    business_attributes: dict | None = Field(default=None, alias="businessAttributes")
    created_by: str | None = Field(default=None, alias="createdBy")
    updated_by: str | None = Field(default=None, alias="updatedBy")
    create_time: int | None = Field(default=None, alias="createTime")
    update_time: int | None = Field(default=None, alias="updateTime")


class AtlasEntityWithExtInfo(_AtlasBase):
    """Entity with extended info including referred entities."""

    entity: AtlasEntity
    referred_entities: dict[str, AtlasEntity] | None = Field(default=None, alias="referredEntities")


class AtlasEntitiesWithExtInfo(_AtlasBase):
    """Bulk entity response with extended info."""

    entities: list[AtlasEntity] | None = None
    referred_entities: dict[str, AtlasEntity] | None = Field(default=None, alias="referredEntities")


# * Search Models


class SearchResultMetadata(_AtlasBase):
    """Metadata about search results (pagination, etc.)."""

    total_count: int | None = Field(default=None, alias="totalCount")
    count: int | None = None


class AtlasSearchResult(_AtlasBase):
    """Result from basic or DSL search."""

    search_parameters: dict | None = Field(default=None, alias="searchParameters")
    query_type: str | None = Field(default=None, alias="queryType")
    query_text: str | None = Field(default=None, alias="queryText")
    type_name: str | None = Field(default=None, alias="typeName")
    entities: list[AtlasEntityHeader] | None = None
    attributes: dict | None = None
    full_text_result: list[dict] | None = Field(default=None, alias="fullTextResult")
    approximate_count: int | None = Field(default=None, alias="approximateCount")


# * Lineage Models


class LineageRelation(_AtlasBase):
    """A single edge in the lineage graph."""

    from_entity_id: str = Field(alias="fromEntityId")
    to_entity_id: str = Field(alias="toEntityId")
    relationship_id: str = Field(alias="relationshipId")


class AtlasLineageInfo(_AtlasBase):
    """Lineage graph for an entity showing upstream/downstream dependencies."""

    base_entity_guid: str = Field(alias="baseEntityGuid")
    lineage_direction: str = Field(alias="lineageDirection")
    lineage_depth: int = Field(alias="lineageDepth")
    guid_entity_map: dict[str, AtlasEntityHeader] | None = Field(
        default=None, alias="guidEntityMap"
    )
    relations: list[LineageRelation] | None = None


# * Glossary Models


class AtlasGlossaryHeader(_AtlasBase):
    """Lightweight glossary reference."""

    glossary_guid: str = Field(alias="glossaryGuid")
    display_text: str | None = Field(default=None, alias="displayText")


class AtlasGlossaryTerm(_AtlasBase):
    """A glossary term with its definition and relationships."""

    guid: str | None = None
    qualified_name: str | None = Field(default=None, alias="qualifiedName")
    name: str | None = None
    short_description: str | None = Field(default=None, alias="shortDescription")
    long_description: str | None = Field(default=None, alias="longDescription")
    anchor: AtlasGlossaryHeader | None = None
    categories: list[dict] | None = None
    assigned_entities: list[AtlasEntityHeader] | None = Field(
        default=None, alias="assignedEntities"
    )
    see_also: list[dict] | None = Field(default=None, alias="seeAlso")


class AtlasGlossary(_AtlasBase):
    """A glossary containing categories and terms."""

    guid: str | None = None
    qualified_name: str | None = Field(default=None, alias="qualifiedName")
    name: str | None = None
    short_description: str | None = Field(default=None, alias="shortDescription")
    long_description: str | None = Field(default=None, alias="longDescription")
    terms: list[AtlasGlossaryTerm] | None = None
    categories: list[dict] | None = None


# * Type Definition Models


class AtlasAttributeDef(_AtlasBase):
    """Definition of an attribute within a type."""

    name: str | None = None
    type_name: str | None = Field(default=None, alias="typeName")
    is_optional: bool | None = Field(default=None, alias="isOptional")
    cardinality: str | None = None
    is_unique: bool | None = Field(default=None, alias="isUnique")
    is_indexable: bool | None = Field(default=None, alias="isIndexable")
    description: str | None = None
    default_value: str | None = Field(default=None, alias="defaultValue")


class AtlasEntityDef(_AtlasBase):
    """Definition of an entity type in Atlas."""

    name: str | None = None
    category: str | None = None
    guid: str | None = None
    description: str | None = None
    type_version: str | None = Field(default=None, alias="typeVersion")
    service_type: str | None = Field(default=None, alias="serviceType")
    attribute_defs: list[AtlasAttributeDef] | None = Field(default=None, alias="attributeDefs")
    super_types: list[str] | None = Field(default=None, alias="superTypes")
    sub_types: list[str] | None = Field(default=None, alias="subTypes")
    relationship_attribute_defs: list[dict] | None = Field(
        default=None, alias="relationshipAttributeDefs"
    )


class AtlasClassificationDef(_AtlasBase):
    """Definition of a classification (tag) type."""

    name: str | None = None
    category: str | None = None
    guid: str | None = None
    description: str | None = None
    attribute_defs: list[AtlasAttributeDef] | None = Field(default=None, alias="attributeDefs")
    super_types: list[str] | None = Field(default=None, alias="superTypes")
    entity_types: list[str] | None = Field(default=None, alias="entityTypes")


class AtlasTypesDef(_AtlasBase):
    """Container for all type definitions."""

    enum_defs: list[dict] | None = Field(default=None, alias="enumDefs")
    struct_defs: list[dict] | None = Field(default=None, alias="structDefs")
    classification_defs: list[AtlasClassificationDef] | None = Field(
        default=None, alias="classificationDefs"
    )
    entity_defs: list[AtlasEntityDef] | None = Field(default=None, alias="entityDefs")
    relationship_defs: list[dict] | None = Field(default=None, alias="relationshipDefs")
    business_metadata_defs: list[dict] | None = Field(default=None, alias="businessMetadataDefs")
