// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/TileStatus.h"

namespace canvas
{
// Where a row's program runs, as its muted line says it: the Engine on the truth's core, a deck,
// the desk and Motion where Core hears them. On this machine "local" with its first address; not
// known to Core, "local" when installed here, else nothing (no guess).
juce::String hostLine (const Tile& tile, const Facts& facts);
}
