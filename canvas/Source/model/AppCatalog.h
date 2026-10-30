// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
enum class TileKind { core, deck, mixer, motion, analyzer };

// One program of the rig as the Canvas shows it: the systemd user units that are it, the package
// that brings it, and the unit whose process owns its window.
struct Tile
{
    TileKind kind;
    juce::String id, label, caption;
    std::vector<juce::String> units;
    juce::String package, windowUnit;
    int deck = 0;   // 1-based for a deck tile, 0 otherwise
};

// The engine's deck names: A … Z, then AA, AB, … (installer/roles/laptop.py deck_letters).
std::vector<juce::String> deckLetters (int count);

// Core, one tile per deck, Mixer, Motion, beat-analyzer.
std::vector<Tile> catalog (int decks);

// [laptop] decks from ~/.config/a3/install.conf: empty, absent or a value the installer refuses
// (not a whole number from 1, or above the truth's range) is the truth's deck count (plan R11).
int decksFromInstallConf (const juce::String& iniText, int truthDecks);

// The upper bound of stemdeck.deck-hello's deck range in a3-osc.json, or `fallback`.
int truthDeckCount (const juce::var& truth, int fallback);
}
