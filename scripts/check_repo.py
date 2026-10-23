#!/usr/bin/env python3
"""Check repository-wide metadata and private-planning-file invariants."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
failures: list[str] = []
passes: list[str] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    target = passes if ok else failures
    target.append(name if not detail else f"{name}: {detail}")


def read_text(relative: str) -> str | None:
    try:
        return (ROOT / relative).read_text(encoding="utf-8")
    except OSError as exc:
        record(f"read {relative}", False, str(exc))
        return None


def git(args: list[str]) -> subprocess.CompletedProcess[str] | None:
    command = ["git", "-c", f"safe.directory={ROOT.as_posix()}", *args]
    try:
        return subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        record("run Git check", False, str(exc))
        return None


def main() -> int:
    raw = read_text("config/app-metadata.json")
    metadata: dict[str, Any] | None = None
    if raw is not None:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and isinstance(parsed.get("project_metadata"), dict):
                metadata = parsed["project_metadata"]
                record("metadata JSON and project_metadata object", True)
            else:
                record("metadata JSON and project_metadata object", False, "expected an object")
        except json.JSONDecodeError as exc:
            record("metadata JSON", False, f"line {exc.lineno}, column {exc.colno}: {exc.msg}")

    if metadata is not None:
        app_name = metadata.get("app_name")
        repository = metadata.get("repository")
        holder = metadata.get("copyright_holder")
        license_id = metadata.get("license")
        required = {
            "app_name": isinstance(app_name, str) and bool(app_name.strip()),
            "description": isinstance(metadata.get("description"), str) and bool(metadata["description"].strip()),
            "repository.owner": isinstance(repository, dict) and bool(repository.get("owner")),
            "repository.name": isinstance(repository, dict) and bool(repository.get("name")),
            "license": isinstance(license_id, str) and bool(license_id.strip()),
            "copyright_holder.name": isinstance(holder, dict) and bool(holder.get("name")),
            "copyright_holder.email": isinstance(holder, dict) and bool(holder.get("email")),
        }
        missing = [key for key, present in required.items() if not present]
        record("required project metadata", not missing, ", ".join(missing))

        readme = read_text("README.md")
        license_text = read_text("LICENSE")
        if readme is not None and isinstance(app_name, str):
            first_heading = next((line.strip() for line in readme.splitlines() if line.strip()), "")
            record("README title matches metadata", first_heading == f"# {app_name}", first_heading)
        if license_text is not None and isinstance(app_name, str):
            lines = license_text.splitlines()
            title_ok = bool(lines) and lines[0].strip() == app_name
            record("LICENSE title matches metadata", title_ok, lines[0].strip() if lines else "empty file")
            holder_ok = False
            spdx_ok = False
            if isinstance(holder, dict):
                expected = f"{holder.get('name', '')} <{holder.get('email', '')}>"
                holder_ok = len(lines) > 1 and lines[1].startswith("Copyright ") and lines[1].endswith(expected)
            record("LICENSE copyright matches metadata", holder_ok)
            spdx = f"SPDX-License-Identifier: {license_id}"
            spdx_ok = any(line.strip() == spdx for line in lines)
            record("LICENSE SPDX matches metadata", spdx_ok, spdx)

    ignored = git(["check-ignore", "--quiet", "--no-index", "dev-assets/agent-docs/agent.md"])
    record("dev-assets is ignored", ignored is not None and ignored.returncode == 0)
    tracked = git(["ls-files", "--", "dev-assets/"])
    tracked_output = tracked.stdout.strip() if tracked is not None else "Git unavailable"
    record("no dev-assets files are tracked", tracked is not None and not tracked_output, tracked_output)

    for name in passes:
        print(f"PASS: {name}")
    for name in failures:
        print(f"FAIL: {name}", file=sys.stderr)
    if failures:
        print(f"Repository check failed: {len(failures)} of {len(passes) + len(failures)} checks.", file=sys.stderr)
        return 1
    print(f"Repository check passed: {len(passes)} checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
