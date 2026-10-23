# Admin Analytics

A modular, configurable business administration platform with a reusable core and separate business domain modules.

## Status

I1 architecture and scope baseline is prepared for review. The repository check is available; no application runtime or rental CRUD has been implemented yet.

## Architecture and scope

- [Architecture](docs/architecture.md)
- [Requirements traceability](docs/requirements-traceability.md)
- [Development workflow](docs/development-workflow.md)
- [Architecture decision record](docs/decisions/ADR-0001-modular-monolith.md)
- [Project timeline](docs/project-timeline.md)
- [Project metadata](config/app-metadata.json)

## Planned technology stack

- Backend: Python, FastAPI and Pydantic.
- Database: PostgreSQL, SQLAlchemy and Alembic.
- Web: React, TypeScript and Vite.
- Configuration: JSON with a versioned schema and semantic validation.
- Local runtime: Docker Compose; add Nginx only when routing/deployment needs it.
- CI and testing: GitHub Actions, pytest and Playwright.
- Native mobile, AI integrations and public websites are deferred.

The stack is a plan. Dependencies and versions will be selected and locked when their implementation increments begin.

## Development check

From the repository root, run:

    python scripts/check_repo.py

This checks project metadata against the README and LICENSE and verifies that local planning files remain ignored. It is not an application test suite; component and runtime checks will be added with those components.

Rental-specific terminology, pricing, calculations and policies belong to the rental domain configuration/module. They must not become reusable-core defaults.
