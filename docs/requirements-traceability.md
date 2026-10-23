# Admin Analytics Requirements Traceability

**Status:** I1 review draft
**Authority:** 05-core-application-requirements.md, derived from source documents 01–04.
**Purpose:** Map every MVP requirement to an owner, increment, source, and boundary.

## Core and platform requirements

| Requirement | Owning component | Increment | Source | Boundary / acceptance focus |
|---|---|---|---|---|
| CORE-001 individual owner/partner accounts | Core identity/access | I5 | 02 §3; 03 §7 | No shared credentials. |
| CORE-002 verified workspace scope | Core authorization | I5 | 02 §3; 03 §4.2, §7.2 | Caller-supplied workspace ID never grants access. |
| CORE-003 disabled account and safe recovery | Core identity/access | I5 | 02 §3; 03 §7.1 | Revocation blocks access; recovery does not expose credentials/documents. |
| CORE-004 attributable sensitive actions | Core audit | I5–I6, extended per domain | 02 §3; 03 §7.4 | Actor, workspace, target and time are recorded; sensitive values redacted. |
| CORE-005 append-only audit for normal users | Core audit/persistence | I5 | 03 §7.4 | Normal application users cannot rewrite history. |
| CORE-006 initial partner access plus future permissions | Core authorization | I5 | 02 §3; 03 §7.2 | Explicit checks; no premature broad role system. |
| CORE-010 strict data-only configuration | Config parser/package | I4 | Master instructions §7; 03 §11 | No execution or dynamic module loading from config. |
| CORE-011 draft validation and preview | Config lifecycle | I4–I6 | Master instructions §7; 03 §12.2 | Invalid draft cannot affect active behavior. |
| CORE-012 explicit activation and revisioned rollback | Config lifecycle | I6 | Master instructions §7; 03 §12.2 | Activation is authorized, atomic and auditable. |
| CORE-013 versioned envelope and module validation | Global config + module registry | I2, I4 | 06–08; 03 §3 | Generic parser stays independent of rental semantics. |
| CORE-014 secret separation | Global config/service settings | I2, I4, I6 | Master instructions §2; 03 §7.3 | No resolved credentials in business config, clients, logs or exports. |
| CORE-015 module isolation | Core/config registry | I4, I6 | Master instructions §3, §7; 03 §3.1 | Rental module cannot bypass core controls or break unrelated core features. |
| CORE-020 responsive accessible UI and time-zone display | Web client + core API | I6, I11 | 02 §15; 03 §5, §13.2 | Labels, keyboard use, contrast, empty/error states. Native mobile deferred. |
| CORE-021 server validation and safe errors | API/core | I3 and every feature increment | 02 §15; 03 §5.1 | Client validation is never authoritative. |
| CORE-022 health/readiness and correlation IDs | API/operations | I3, I12 | 03 §5.1, §14 | Readiness reflects required dependencies; logs omit personal/secret data. |
| CORE-023 core workflows independent of nonessential providers | Core/integration adapters | I3, I11 | 02 §1, §16; 03 §1, §21 | Provider outage does not prevent ordinary administration. |
| CORE-024 stage-specific operating documentation | Root/docs + owning component | I1–I12 | Master instructions §12; 03 §21 | Setup/runbook changes accompany behavior and operational changes. |

## Rental-domain requirements

| Requirement | Owning component | Increment | Source | Boundary / acceptance focus |
|---|---|---|---|---|
| RENT-001 customer profile and multiple phones | Rental customers | I7 | 02 §5.2, §6.1 | Stable internal ID; phone numbers are searchable, not unique identity. |
| RENT-002 duplicate suggestions, human resolution | Rental customers | I7 | 02 §5.2, §6.1, §15 | Never silently merge. |
| RENT-003 evidence-backed referral attribution | Rental referrals/finance | I7, I10 | 01 §10; 02 §5.2, §9 | Independent repeat booking does not automatically earn commission. |
| RENT-004 vehicle lifecycle and downtime | Rental vehicles | I7, I12 | 02 §5.3, §7; 03 §4.1 | One-vehicle pilot, multi-vehicle-safe records. |
| RENT-005 attributable odometer and correction | Rental vehicles/bookings | I7, I9 | 02 §7.2, §8.1 | Decreases require privileged correction. |
| RENT-006 conflict-safe availability | Rental bookings/vehicles | I9 | 02 §8.2 | Confirmed overlap and blocked periods cannot silently conflict. |
| RENT-007 defined booking state transitions | Rental bookings | I9 | 02 §8; 03 §5.3 | Exact policy approved before use. |
| RENT-008 immutable quote-rule snapshot | Rental pricing/bookings | I9 | 02 §8.1–8.3; 03 §4.3 | Policy changes do not rewrite historical quote. |
| RENT-009 deterministic mileage/rental charges | Rental calculation service | I9 | 02 §8.3; 03 §6 | Exact day/proration/late-return rules remain a blocker until decided. |
| RENT-010 deposits separated as liabilities | Rental finance | I10 | 01 §3.2; 02 §9.1; 03 §4.3 | Collection/refund/application are explicit transactions. |
| RENT-011 decimal-safe payments, expenses and reconciliation | Rental finance | I10 | 02 §9–10; 03 §4.3, §6 | No autonomous external money movement. |
| RENT-012 unique versioned commission accrual | Rental referrals/finance | I10 | 01 §10; 02 §9.2; 03 §6 | Refunds/adjustments preserve history; retry cannot duplicate. |
| RENT-013 private inspection and document evidence | Document service + rental inspections | I8, I9 | 02 §6; 03 §8 | Authorization, quarantine/validation and access audit. |
| RENT-014 distinguish finance measures in reports | Rental reporting | I10, I11 | 01 App A; 02 §12, §14; 03 §6, §10 | Revenue, cash, deposits, operating and economic result are labelled separately. |
| RENT-015 authorized auditable export | API/reporting | I11 | 02 §14; 03 §5.1 | Sensitive export is permission-checked and audited. |

## Deferred or conditional requirements

| Capability | Status | Reason / revisit point |
|---|---|---|
| Native Android/iOS clients and offline writes | Deferred | Master instructions require explicit scope; responsive web first. Revisit after I11 pilot evidence. |
| Budgets, rolling forecasts, scenarios and broad KPI dashboards | Later product phase | Explicitly outside the operational web MVP in I11; prioritize after reliable transaction data. |
| AI/agent workflows | Deferred | Master instructions and 03 §11 require a separate approved milestone, provider/data review and human controls. |
| Payment gateway, bank sync, customer messaging | Deferred | Not required for recordkeeping MVP; external side effects need their own risk approval. |
| Customer login/public booking/contract signing/tax filing/telematics | Excluded | 02 §2.2; no current approved increment. |
| Cloud deployment and production release | Conditional/future | I12 is staging/recovery readiness; production release requires a separate approval and verified cost/security decisions. |

## Blocking policy decisions

I9 cannot finalize its state machine or charges until rental-day, partial-day/late-return, package-extension/proration and odometer-correction rules are decided. I10 cannot finalize deposits, revenue recognition, commission rounding/disputes, reserve/accounting categories or approval policy until the owner approves those rules. I8 needs document types/retention and a storage approach before production use. These are not defaulted by the core.
