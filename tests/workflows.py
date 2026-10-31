# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Plain text views of the workflow files under .github/workflows.

There is no YAML library here, and adding one is a dependency.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO / ".github" / "workflows"
PACKAGES = WORKFLOWS / "packages.yml"
BUILD_PACKAGES = WORKFLOWS / "build-packages.yml"
RELEASE_DEBS = WORKFLOWS / "release-debs.yml"
JOB_INDENT = "  "


def all_workflows():
    return sorted(WORKFLOWS.glob("*.yml"))


def top_block(text, key):
    """The lines of a top-level `key:` up to the next top-level key."""
    found = re.search(rf"(?ms)^{key}:[^\n]*\n(.*?)(?=^\S|\Z)", text)
    return found.group(1) if found else ""


def job_blocks(text):
    """Each job's lines, keyed by name: a job starts at two-space indent under `jobs:`."""
    blocks, current, in_jobs = {}, None, False
    for line in text.splitlines():
        if line.startswith("jobs:"):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            break
        heading = re.match(rf"^{JOB_INDENT}([A-Za-z0-9_-]+):\s*$", line)
        if heading:
            current = heading.group(1)
            blocks[current] = []
        elif current:
            blocks[current].append(line)
    return {name: "\n".join(lines) for name, lines in blocks.items()}


def run_commands(text):
    """Every command line of every `run:`, inline or in a `run: |` block."""
    commands, block_indent = [], None
    for line in text.splitlines():
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if block_indent is not None:
            if stripped and indent < block_indent:
                block_indent = None
            elif stripped:
                commands.append(stripped)
                continue
        found = re.match(r"^\s*(?:- )?run:\s*(.*)$", line)
        if not found:
            continue
        if found.group(1) in ("|", ">"):
            block_indent = indent + 2
        else:
            commands.append(found.group(1))
    return commands
