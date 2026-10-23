# Admin Analytics Development Workflow

**Status:** I1 review draft
**Local baseline command:** python scripts/check_repo.py
**Runtime commands:** Add with the first implemented runtime component; no app run configuration exists yet.

## Root check ownership

Run python scripts/check_repo.py from the repository root. It uses the Python standard library and checks only repository-wide invariants that exist today:

- config/app-metadata.json parses and contains the project identity fields needed by the repository.
- The README title and LICENSE attribution/SPDX header agree with that metadata.
- The root ignore rule excludes dev-assets/ and no dev-assets/ files are tracked.

The command is a repository-level check, not an application test suite. It does not validate the business configuration schema, start a service, access Docker, test a database, or perform an external GitHub operation. A failing check prints a concise failure and exits nonzero.

When components are introduced, each component owns its own commands and checks. Root orchestration should call those documented commands, preserve their exit codes, and report failures; it should not duplicate domain validation or tests.

## Planned command conventions

| Component | Command convention | When introduced |
|---|---|---|
| Repository baseline | python scripts/check_repo.py | I1 |
| Python API and packages | Document exact locked-environment commands in the component README and pyproject configuration | I3/I4 |
| Web client | Document package-manager commands in apps/web/README and its package manifest | When web runtime is approved |
| Database migrations | Use Alembic through the API service's documented environment | I3 |
| Local container environment | Document Docker Compose commands only after its services and health checks exist | I3/I12 as needed |
| CI | Invoke root orchestration and component-owned checks with least privilege | I2 onward |

Do not add speculative package scripts or empty components to make a convention look complete.

## Run configurations

There is no application process to launch yet. Do not create editor launch profiles, VS Code tasks, Docker service definitions, or environment files until the corresponding runtime entry point and environment contract exist. When I3 adds FastAPI and PostgreSQL, document one safe local launch path and provide non-secret examples. Keep secrets out of editor settings committed to Git.

## Feature and review cycle

1. Confirm the approved milestone, clean/understood worktree, and current develop base.
2. Work on a descriptive feature branch. Do not rewrite shared history or discard unmerged work.
3. Keep the diff within the increment, update relevant docs, run root and component checks, and review for secrets and ignored files.
4. Commit with the project message format and update ignored dev-assets/commit-notes.md with actual hash, timestamp, scope and results.
5. Stop at the increment's review gate. The owner manually creates/reviews/merges PRs. A PR or merge is never claimed without verification.
6. After the owner reports a merge, verify merged history before starting the next increment.

GitHub fetch/push and CI configuration may remain unavailable until the owner completes GitHub CLI authentication and network access is available. Local checks and documentation work do not require that authentication.
