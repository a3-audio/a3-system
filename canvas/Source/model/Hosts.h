// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/TileStatus.h"

namespace canvas
{
// Where a row's program runs, as its muted line says it: where Core hears it (deck, desk, Motion),
// else the machine the truth names for the role (core, deckhost-<letter>, mixer, motion). On this
// machine "local" with its control and audio network addresses; named by neither, nothing (no guess).
juce::String hostLine (const Tile& tile, const Facts& facts);

// Whether the program runs on this machine: its address is one of this machine's, or nobody names one.
bool runsHere (const Tile& tile, const Facts& facts);
// Its version: this machine's package where it runs here ("not installed" without one); elsewhere
// "not reported" (no device tells Core its version yet).
juce::String softwareLine (const Tile& tile, const Facts& facts);
// The firmware of its device: empty for a program without one (only the Mixer's Pico and Motion's
// ESP32 panel have firmware). Neither device reports it; on Motion's own machine the installer's record
// of what it flashed stands in: the system's tag when it is the pinned firmware, else its tree.
juce::String firmwareLine (const Tile& tile, const Facts& facts);
}
