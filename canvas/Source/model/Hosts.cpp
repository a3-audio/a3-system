// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Hosts.h"

namespace canvas
{
namespace
{
juce::String truthHost (const NetworkFacts& network, const juce::String& name)
{
    const auto host = network.truth.hosts.find (name);
    return host != network.truth.hosts.end() ? host->second : juce::String();
}

// Deck 1 is "deckhost-a": the truth names each deck's machine by its letter.
juce::String deckHostName (int deck)
{
    return "deckhost-" + juce::String::charToString ((juce::juce_wchar) ('a' + deck - 1));
}

// Core's live report first, then the machine the truth names for the role.
juce::String knownAddress (const Tile& tile, const Facts& facts)
{
    const auto& network = facts.network;
    switch (tile.kind)
    {
        case TileKind::core: return truthHost (network, "core");
        case TileKind::analyzer: return truthHost (network, "core");
        case TileKind::deck:
        {
            const auto deck = facts.core.deckHosts.find (tile.deck);
            return deck != facts.core.deckHosts.end() ? deck->second : truthHost (network, deckHostName (tile.deck));
        }
        case TileKind::mixer: return facts.core.deskHost.isNotEmpty() ? facts.core.deskHost : truthHost (network, "mixer");
        case TileKind::motion: return facts.core.motionHost.isNotEmpty() ? facts.core.motionHost : truthHost (network, "motion");
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

}

juce::String hostLine (const Tile& tile, const Facts& facts)
{
    const auto address = knownAddress (tile, facts);
    if (address.isNotEmpty())
        return isOwn (address, facts.network) ? local (facts.network) : address;
    return {};   // neither Core nor the truth names it: no guess, it would be no status
}
}
