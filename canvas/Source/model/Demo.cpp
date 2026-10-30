// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Demo.h"

namespace canvas
{
namespace
{
const juce::String demoVersion = "03.0";

UnitFacts runningUnit (int pid) { return { "loaded", "active", "running", "success", pid }; }
UnitFacts stoppedUnit() { return { "loaded", "inactive", "dead", "success", 0 }; }
}

Snapshot demoSnapshot (const std::vector<Tile>& tiles)
{
    int lastDeck = 0;
    for (const auto& tile : tiles)
        lastDeck = std::max (lastDeck, tile.deck);

    Snapshot snapshot;
    auto& facts = snapshot.facts;
    int pid = 2100;
    for (const auto& tile : tiles)
    {
        facts.packages[tile.package] = { demoVersion, demoVersion };
        const bool stopped = tile.kind == TileKind::deck && tile.deck == lastDeck;
        for (const auto& unit : tile.units)
            facts.units[unit] = stopped ? stoppedUnit() : runningUnit (pid++);
        if (tile.kind == TileKind::deck && ! stopped)
            facts.core.presentDecks.insert (tile.deck);
    }
    facts.core.reachable = true;
    facts.core.engineHeard = true;
    facts.engine.answers = true;
    facts.engine.sampleRate = 44100;   // the rig: 44.1 kHz, 128 frames
    facts.engine.blockSize = 128;
    facts.engine.dspLoadPercent = 14.0f;
    for (const auto& tile : tiles)
        snapshot.statuses.push_back (statusOf (tile, facts));
    return snapshot;
}

int DemoRunner::run (const juce::StringArray& argv, const LineCallback& line)
{
    if (line)
        line ("demo, not run: " + argv.joinIntoString (" "));
    return 0;
}
}
