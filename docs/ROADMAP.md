# Roadmap

Feature gap analysis based on [Apache Atlas REST API v2](https://atlas.apache.org/api/v2/index.html).

## Priority 1 — Core Governance Features

### Entity Audit History

`GET /v2/entity/{guid}/audit`

Query who changed what and when. Returns `EntityAuditEventV2` with action type (ENTITY_CREATE, ENTITY_UPDATE, CLASSIFICATION_ADD, etc.), timestamp, user, and entity snapshot at change time.

- Single endpoint, low implementation cost
- Answers the fundamental governance question: "Who modified this entity and when?"

### Relationship REST

`GET/POST/PUT/DELETE /v2/relationship/guid/{guid}`, `POST /v2/relationship`

Relationships are first-class objects in Atlas with their own GUIDs (e.g., table→column, process→input/output). Currently not implemented at all.

- Direct structural navigation between entities
- Create/modify relationships for metadata curation
- Required for complete metadata graph understanding

### Business Metadata

`GET/POST/DELETE /v2/entity/guid/{guid}/businessmetadata/{bmName}`

Namespaced, typed custom attributes added in Atlas 2.x. Unlike classifications (tags), business metadata carries structured values (e.g., `DataQuality.completeness = 0.95`, `DataStewardship.owner = "data-eng-team"`).

- Read and write custom governance attributes
- Also requires `GET /v2/types/businessmetadatadef/name/{name}` for schema introspection

## Priority 2 — Practical Enhancements

### Glossary Term ↔ Entity Assignment

`GET/POST/DELETE /v2/glossary/terms/{termGuid}/assignedEntities`

Link business terms to physical assets. Answers: "Which tables/columns implement this business concept?"

### Entity Labels

`POST/PUT/DELETE /v2/entity/guid/{guid}/labels`

Lightweight string tags (unlike typed classifications). Useful for operational markers like "needs-review" or external system IDs.

### Relationship Search

`GET /v2/search/relationship`

Find entities connected to a specific entity by relationship type. More intuitive than DSL for structural queries like "all hive_tables in this hive_db".

### Classification Update

`PUT /v2/entity/guid/{guid}/classifications`

Currently only add (POST) and remove (DELETE) are supported. PUT allows modifying classification attributes (e.g., confidence score, expiry date).

## Priority 3 — Future Additions

### Glossary Categories

- `GET /v2/glossary/{glossaryGuid}/categories`
- `GET /v2/glossary/category/{categoryGuid}`
- `GET /v2/glossary/category/{categoryGuid}/terms`

Hierarchical taxonomy navigation (e.g., Finance > Revenue > ARR).

### TypeDef Extensions

- `GET /v2/types/relationshipdef/name/{name}` — relationship type schema (needed for Relationship REST)
- `GET /v2/types/businessmetadatadef/name/{name}` — business metadata schema
- `GET /v2/types/typedefs/headers` — lightweight type list (name + guid only)
- `GET /v2/types/enumdef/name/{name}` — allowed value lists

### Glossary Write Operations

- `POST /v2/glossary/term` — create term
- `PUT /v2/glossary/term/{termGuid}` — update term

### Bulk Operations

- `POST /v2/entity/bulk` — batch create/update entities
- `DELETE /v2/entity/bulk` — batch delete
- `POST /v2/entity/bulk/classification` — apply classification to multiple entities

## Priority 4 — Performance

### Local Metadata Cache

Cache frequently accessed metadata (entity details, lineage, type definitions) in a local SQLite database to reduce API calls and improve response time. Useful when agents make repeated queries against the same catalog.

- Configurable TTL for cache invalidation
- Optional — disabled by default to keep the server stateless
- Community-suggested feature

## Intentionally Excluded

| Endpoint | Reason |
|---|---|
| Saved searches (POST/PUT/DELETE) | Server-side state — poor fit for MCP session-based tools |
| Business metadata CSV import | Multipart upload — not suitable for LLM agent workflows |
| Glossary CSV import | Same reason |
| IndexRecoveryREST | Admin operations only |
| NotificationREST | Pub/sub — no MCP tool equivalent |
| Search download endpoints | Async file generation — poor fit for agent workflows |
