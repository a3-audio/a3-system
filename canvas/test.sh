#!/bin/bash
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The Canvas's tests: build, then run what was just built, on a screen of its own.
#
#   ./test.sh [-- CTEST ARGS]          e.g. ./test.sh -- -R StartPlan
#
# ctest runs a binary, it does not build one: this builds first and prints when
# the runner was built. The tests run no systemctl, apt or pkexec: every
# command goes to a fake runner.
# A3CANVAS_BUILD moves the build directory (default: build/ beside this file).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BUILD="${A3CANVAS_BUILD:-$HERE/build}"
CTEST_ARGS=()
if [[ "${1:-}" == "--" ]]; then shift; CTEST_ARGS=("$@"); fi

nice -n 19 cmake -S "$HERE" -B "$BUILD" -DCMAKE_BUILD_TYPE=Release -DA3CANVAS_TESTS=ON \
    -DCMAKE_PREFIX_PATH="$HOME/local/juce"
nice -n 19 cmake --build "$BUILD" -j2

RUNNER="$BUILD/tests/a3-canvas-tests_artefacts/Release/a3-canvas-tests"
echo "=== runner built $(date -r "$RUNNER" '+%Y-%m-%d %H:%M:%S') ==="

RUN=(ctest --test-dir "$BUILD" --output-on-failure "${CTEST_ARGS[@]}")
if command -v xvfb-run >/dev/null; then xvfb-run -a "${RUN[@]}"; else "${RUN[@]}"; fi
