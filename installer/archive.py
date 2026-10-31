# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The public apt archive: where it is, which suite a machine takes, and the
command that runs the root helper.

installer/a3-root cannot import this file (it is copied alone), so it carries
its own copy of these values; tests/test_a3_root.py pins that both agree.
"""

from pathlib import Path

ARCHIVE_URL = "https://a3-audio.github.io/a3-system"
KEYRING = Path("/usr/share/keyrings/a3-audio.gpg")
SOURCES = Path("/etc/apt/sources.list.d/a3-audio.sources")
SUITES = ("forky", "trixie")
A3_PACKAGES = ("a3-core", "a3-core-app", "stemdeck", "a3-desk",
               "a3-motion-ui", "beat-analyzer", "a3-update")

A3_ROOT = Path(__file__).resolve().parent / "a3-root"


class ArchiveError(Exception):
    pass


def suite_for(os_release):
    codename = os_release.get("VERSION_CODENAME", "")
    if codename in SUITES:
        return codename
    raise ArchiveError(
        f"The A3 archive has packages for {' and '.join(SUITES)}; this machine "
        f"reports VERSION_CODENAME={codename or '(none)'}. Debian testing without "
        "a codename needs the suite chosen by hand.")


def sources_text(suite):
    if suite not in SUITES:
        raise ArchiveError(f"No archive suite {suite!r}; there is {' and '.join(SUITES)}.")
    return "\n".join([
        "Types: deb",
        f"URIs: {ARCHIVE_URL}",
        f"Suites: {suite}",
        "Components: main",
        f"Signed-By: {KEYRING}",
        "",
    ])


def a3_root_command(ctx, verb, *args):
    """The helper's command line, without sudo: callers run it with root=True."""
    return [str(A3_ROOT), verb, *args]
