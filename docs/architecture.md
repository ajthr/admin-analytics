# Admin Analytics Architecture

**Status:** I1 review draft
**Scope:** Approved planning baseline for the reusable platform core and separately configured self-drive-rental domain.

## Architecture summary

Admin Analytics starts as a modular monolith in a single repository. The server owns business rules, authorization, financial calculations, and persistence. Web clients use a versioned API. Project metadata, deployment settings, and business configuration have separate sources and lifecycles.

Dependency direction:

- The orchestration layer calls project- or component-owned commands; it does not own business rules.
- UI clients depend on the API contract, not database tables or domain implementations.
- API routes depend on application services. Services enforce authorization and call domain operations.
- Domain modules depend on shared core interfaces for identity, persistence transactions, audit, and configuration access. The core does not import rental policies.
- The configuration parser depends on the versioned envelope and registered module schemas. It has no dependency on FastAPI or PostgreSQL.
- Infrastructure and provider adapters are called through narrow interfaces. Nonessential providers can fail without stopping core administration.

## Component hierarchy

| Stage | Component | Responsibility and boundary | MVP status |
|---|---|---|---|
| 1 | Root orchestration | Repository-level checks, thin developer/CI commands, release coordination and cross-component docs. No rental policy or domain calculations. | Minimal repository check now; CI orchestration grows with real component checks. |
| 2 | Global project metadata and service settings | Project name, repository identity, license/copyright metadata, component registry and safe service configuration. Secrets are injected per service and never bundled into client/public output. | Metadata exists in config/app-metadata.json. Branch-aware verification/synchronization is I2. |
| 3 | Core application | FastAPI API, identity/workspaces, authorization, shared record lifecycle, validation, audit, transactions, database migrations, diagnostics and safe file-service abstractions. | Foundation I3–I6; reusable services continue as domain increments require. |
| 4 | UI clients | Responsive React/TypeScript/Vite web client consumes OpenAPI/API contracts. It must not duplicate authoritative business rules. | Responsive web in MVP. Native Android/iOS is deferred. |
| 5 | Independent helper packages | Versioned JSON envelope parser, domain-schema registry interface, semantic validation, developer tools and generated/typed API client when needed. | Business-config parser in I4; SDKs and agentic/LLM tools deferred. |
| 6 | App-specific websites | Marketing, public landing pages, blogs and independent documentation sites. | Future only; not part of the product MVP. |
| 7 | Supporting infrastructure | PostgreSQL, Alembic, Docker-based local environment, optional Nginx, CI, private object storage, backups, monitoring and recovery. | Add only with the increments that need each capability; staging/recovery in I12. |

## Interfaces and data flow

- Web client → HTTPS JSON API → FastAPI route → authorized application service → domain operation → transaction/repository → PostgreSQL.
- API contracts are versioned under /api/v1 and described through OpenAPI. The web client consumes generated or otherwise typed contracts; the contract is the boundary, not shared database code.
- A configuration import enters a pure parser: strict JSON syntax → shared envelope schema → trusted module registry → module schema → semantic validation → normalized draft. An authenticated lifecycle service owns preview, activation, history and rollback.
- A domain module can request core identity, workspace checks, transaction, audit, file-storage and configuration interfaces. It cannot bypass those controls.
- Private document metadata is stored with application records. File bytes use private object storage behind an authorization-aware adapter; storage provider choice is deferred until deployment requirements are verified.
- Background work uses an application-owned job interface only when retries, scheduling or workload justify it. A specific queue technology is not selected yet.

## Responsibility boundaries

### Core owns

Identity and workspace membership; deny-by-default authorization hooks; stable non-semantic IDs; shared timestamps and safe error handling; database transactions and migration conventions; audit event capture and redaction; configuration envelope and lifecycle contracts; health/readiness; and common client/API conventions.

### Self-drive-rental domain owns

Customer/referral/vehicle/booking/inspection/payment/deposit/refund/expense/commission concepts; rental state transitions; rental day and package rules; mileage and rental charge calculations; commission eligibility; rental-specific alerts and reports; and the sample Kochi/Ernakulam business configuration.

Rental prices, cost assumptions, reserves, depreciation, business terminology and policy remain domain configuration or domain-module behavior. They are not core defaults. Open or conflicting source assumptions cannot become active policies through silent defaults.

## Proposed repository layout

Only files justified by the approved increments should be created. This is a target structure, not a requirement to create empty directories.

    config/
      app-metadata.json
    apps/
      web/
    services/
      api/
        app/
          api/
          core/
          domains/
          db/
          jobs/
          integrations/
    packages/
      business-config/
      api-client/
    scripts/
      check_repo.py
    infra/
      docker/
      deployment/
      monitoring/
    docs/
      architecture.md
      requirements-traceability.md
      development-workflow.md
      decisions/
    .github/
      workflows/

The local source and agent-planning documents under dev-assets/ remain ignored and must not enter commits. The first runtime directories are added only in the increment that implements them.

## Current MVP and deferred scope

M1 (I0–I6) establishes metadata, repository checks, approved boundaries, API/database diagnostics, independent configuration validation, workspace access/audit, and configuration administration. It does not contain rental CRUD.

The operational web MVP (I7–I12) supports one-vehicle pilot workflows with a data model safe for multiple vehicles: customer/referral/vehicle records, private evidence, bookings/checkout/return, financial records and reconciliation, basic operational reports, responsive web, and staging/recovery readiness.

Deferred: native mobile, offline writes, customer portal and public booking, autonomous money movement, tax/accounting replacement, AI agents, advanced predictive analytics, cloud-provider lock-in, microservices, public marketing sites, production release, and integrations not justified by measured need.

## Architectural constraints

1. Project metadata, deployment secrets, and business settings never share one unrestricted configuration file.
2. Business configuration is data, never executable code. Shared-envelope validation and module-specific validation are distinct.
3. Authorization is enforced server-side on every protected operation and scoped to a verified workspace.
4. Financial values use decimal-safe types and deterministic, versioned calculation services. Deposits, revenue, expenses, and cash movements are distinct.
5. Important records and active configuration revisions are attributable and historically reviewable. Corrections use explicit adjustments or new revisions.
6. Keep the modular monolith until measured scale, independent deployment needs, or team ownership justify service separation.
7. Use stable, maintained dependencies and verify versions, costs, privacy, residency and recovery characteristics at implementation time.
