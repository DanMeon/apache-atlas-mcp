# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-03-30

### Changed

- `ATLAS_BASE_URL` is now a required configuration field (no default value)
- README examples use placeholder values (`your-atlas-server`, `your-username`) for clarity
- Added community-built disclaimer to README

### Added

- SVG banner and search demo screenshot in README
- `.mcp.json` added to `.gitignore`

## [0.1.0] - 2026-03-29

### Added

- Initial public release
- 20 MCP tools across 5 domains: entity search, lineage, classifications, glossary, type definitions
- Read-only by default with explicit `--write` flag for write operations
- Async HTTP client using httpx
- Pydantic V2 response models
- CI pipeline with ruff, pyright, and pytest (Python 3.11/3.12/3.13)

[0.1.1]: https://github.com/DanMeon/apache-atlas-mcp/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/DanMeon/apache-atlas-mcp/releases/tag/v0.1.0
