// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/TileStatus.h"

namespace canvas
{
// Where a row's program runs, as its muted line says it: where Core hears it (deck, desk, Motion),
// else the machine the truth names for the role (core, deckhost-<letter>, mixer, motion). On this
// machine "local" with its first address; named by neither, "local" when installed here, else
// nothing (no guess).
juce::String hostLine (const Tile& tile, const Facts& facts);
}
