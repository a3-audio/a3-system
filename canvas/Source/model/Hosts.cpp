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

// "local", this machine's address on the control network (else its first) and on the audio network.
juce::String local (const NetworkFacts& network)
{
    const auto dot = juce::String::fromUTF8 (" · ");
    juce::String control, audio;
    for (const auto& address : network.own)
    {
        if (audio.isEmpty() && inSubnet (address, network.truth.audio))
            audio = address;
        else if (control.isEmpty())
            control = address;
    }
    juce::String line ("local");
    if (control.isNotEmpty())
        line << dot << control;
    if (audio.isNotEmpty())
        line << dot << "audio " << audio;
    return line;
}

const juce::String notReported = "not reported";
}

juce::String hostLine (const Tile& tile, const Facts& facts)
{
    const auto address = knownAddress (tile, facts);
    if (address.isNotEmpty())
        return isOwn (address, facts.network) ? local (facts.network) : address;
    return {};   // neither Core nor the truth names it: no guess, it would be no status
}

bool runsHere (const Tile& tile, const Facts& facts)
{
    const auto address = knownAddress (tile, facts);
    return address.isEmpty() || isOwn (address, facts.network);
}

juce::String softwareLine (const Tile& tile, const Facts& facts)
{
    if (! runsHere (tile, facts))
        return notReported;
    const auto package = facts.packages.find (tile.package);
    const auto installed = package != facts.packages.end() ? package->second.installed : juce::String();
    return installed.isNotEmpty() ? installed : juce::String ("not installed");
}

juce::String firmwareLine (const Tile& tile, const Facts& facts)
{
    if (tile.kind != TileKind::mixer && tile.kind != TileKind::motion)
        return {};
    const auto& flashed = facts.flashedMotionFirmware;
    if (tile.kind == TileKind::mixer || flashed.isEmpty() || ! runsHere (tile, facts))
        return notReported;
    if (flashed == facts.system.motionFirmwareTree && facts.system.motionFirmwareTag.isNotEmpty())
        return facts.system.motionFirmwareTag;
    return "tree " + flashed.substring (0, 7);
}
}
