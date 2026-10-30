// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Hosts.h"

namespace canvas
{
namespace
{
juce::String knownAddress (const Tile& tile, const Facts& facts)
{
    switch (tile.kind)
    {
        case TileKind::core:
        {
            const auto core = facts.network.truth.hosts.find ("core");
            return core != facts.network.truth.hosts.end() ? core->second : juce::String();
        }
        case TileKind::deck:
        {
            const auto deck = facts.core.deckHosts.find (tile.deck);
            return deck != facts.core.deckHosts.end() ? deck->second : juce::String();
        }
        case TileKind::mixer: return facts.core.deskHost;
        case TileKind::motion: return facts.core.motionHost;
        case TileKind::analyzer: return {};
    }
    return {};
}

bool isOwn (const juce::String& address, const NetworkFacts& network)
{
    return isLoopback (address) || std::find (network.own.begin(), network.own.end(), address) != network.own.end();
}

juce::String local (const NetworkFacts& network)
{
    return network.own.empty() ? juce::String ("local") : "local" + juce::String::fromUTF8 (" · ") + network.own.front();
}

bool installedHere (const Tile& tile, const Facts& facts)
{
    const auto package = facts.packages.find (tile.package);
    return package != facts.packages.end() && package->second.installed.isNotEmpty();
}
}

juce::String hostLine (const Tile& tile, const Facts& facts)
{
    const auto address = knownAddress (tile, facts);
    if (address.isNotEmpty())
        return isOwn (address, facts.network) ? local (facts.network) : address;
    return installedHere (tile, facts) ? local (facts.network) : juce::String();
}
}
