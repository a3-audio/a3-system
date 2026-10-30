// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "TileStatus.h"

namespace canvas
{
namespace
{
juce::String shortName (const juce::String& unit)
{
    return unit.upToLastOccurrenceOf (".service", false, false);
}

UnitFacts factsOf (const Facts& facts, const juce::String& unit)
{
    const auto found = facts.units.find (unit);
    return found != facts.units.end() ? found->second : UnitFacts { "not-found", "inactive", "dead", "success", 0 };
}

bool isStarting (const juce::String& active) { return active == "activating" || active == "reloading"; }

juce::String rateLine (const EngineFacts& engine)
{
    juce::String line = juce::String::fromUTF8 ("Running");
    if (engine.sampleRate > 0)
        line << juce::String::fromUTF8 (" · ") << juce::String (engine.sampleRate / 1000.0, engine.sampleRate % 1000 == 0 ? 0 : 1)
             << " kHz" << juce::String::fromUTF8 (" · ") << engine.blockSize
             << juce::String::fromUTF8 (" · DSP ") << juce::roundToInt (engine.dspLoadPercent) << " %";
    return line;
}

// All of the tile's units are active: what Core and the engine add to that.
TileStatus whenAllRunning (const Tile& tile, const Facts& facts)
{
    if (tile.kind == TileKind::core)
    {
        if (! facts.engine.answers)
            return { Light::degraded, "Engine not answering" };
        if (! facts.engine.running())
            return { Light::degraded, "Engine: " + facts.engine.problem };
        return { Light::running, rateLine (facts.engine) };
    }
    if (tile.kind == TileKind::deck && facts.core.reachable && facts.core.presentDecks.count (tile.deck) == 0)
        return { Light::degraded, "Running, no audio link" };
    return { Light::running, "Running" };
}

TileStatus fromUnits (const Tile& tile, const Facts& facts)
{
    int active = 0;
    juce::String firstDown;
    bool starting = false;
    for (const auto& unit : tile.units)
    {
        const auto state = factsOf (facts, unit);
        if (state.active == "failed")
            return { Light::failed, shortName (unit) + " failed (" + state.result + ")" };
        if (isStarting (state.active))
            starting = true;
        else if (state.active == "active")
            ++active;
        else if (firstDown.isEmpty())
            firstDown = unit;
    }
    if (starting)
        return { Light::starting, juce::String::fromUTF8 ("Starting…") };
    if (active == static_cast<int> (tile.units.size()))
        return whenAllRunning (tile, facts);
    if (active > 0)
        return { Light::degraded, shortName (firstDown) + " not running" };
    return { Light::stopped, "Stopped" };
}
}

TileStatus statusOf (const Tile& tile, const Facts& facts)
{
    const auto package = facts.packages.find (tile.package);
    const bool installed = package != facts.packages.end() && package->second.installed.isNotEmpty();
    auto status = installed ? fromUnits (tile, facts) : TileStatus { Light::missing, "Not installed (" + tile.package + ")" };
    status.updateAvailable = installed && package->second.updateAvailable();
    if (tile.windowUnit.isNotEmpty())
        status.windowPid = factsOf (facts, tile.windowUnit).mainPid;
    return status;
}
}
