# ADR-0001: Modular Monolith and Domain Configuration Boundary

**Status:** Proposed for I1 manual review
**Date:** 24 October 2026
**Owners:** Project owner and maintainers

## Context

The initial product combines a private business administration core with a self-drive-rental business domain. Source 02 describes one initial rental operation and partner collaboration. Source 03 recommends a modular monolith and warns against microservices and complex event streaming before measured need. The project master requires reusable core behavior and rental-specific rules/configuration to stay separate.

## Decision

1. Start with one deployable modular monolith, one PostgreSQL database, and one versioned JSON API.
2. Keep API/transport, core services, domain modules, persistence, integrations, jobs, and UI clients in explicit folders and dependency directions.
3. Make the responsive web client the first user client. Do not create native mobile clients until separately justified and approved.
4. Treat project metadata, service/environment settings, and business configuration as separate sources with separate validation and secret rules.
5. Use a generic, versioned business-configuration envelope with a trusted registry of domain-owned schemas and semantic validators. Keep rental settings and calculations in the rental domain.
6. Store and calculate monetary amounts using decimal-safe types and transactional service operations; keep deterministic calculation logic authoritative.
7. Add infrastructure and providers only when the increment requires them. No deployment cloud, queue, object-storage provider, or reverse proxy is selected by this ADR.

## Alternatives considered

- **Microservices from the start:** rejected for the pilot because they add operational and transaction complexity without evidence of independent scaling/team ownership.
- **Rental-only application with rental concepts in core:** rejected because it would make future business domains dependent on one business's terminology and policies.
- **Generic plugin execution from configuration:** rejected because configuration must remain data and must not select executable code or arbitrary permissions.
- **Native mobile as a day-one requirement:** deferred because it increases delivery and release burden before responsive-web workflows are validated.
- **Warehouse/event streaming immediately:** deferred; PostgreSQL and explicit service boundaries are sufficient for the current scale assumptions.

## Consequences

Positive: smaller operational footprint; a clear boundary for rental rules; simpler financial transactions; one API contract; and a path to additional domain modules without premature services.

Costs and constraints: module boundaries need code review; the monolith still requires strict workspace isolation; clients depend on API contracts; and a later service split will require measured evidence and an explicit migration plan.

## Revisit when

Reassess if a domain needs independent deployment/scaling, teams need separate ownership, a demonstrated workload exceeds the monolith's limits, native field workflows are validated as necessary, or operational/cloud constraints change. Revisit provider choices after current pricing, region, privacy, backup and recovery requirements are checked.
