// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "Fixtures.h"
#include "model/Demo.h"
#include "model/Hosts.h"
#include "model/Network.h"

using namespace canvas;

namespace
{
TruthNetwork fixtureTruth() { return parseTruthNetwork (juce::JSON::parse (fixture ("truth-network.json"))); }

Tile tileOf (const juce::String& id)
{
    for (const auto& tile : catalog (4))
        if (tile.id == id)
            return tile;
    ADD_FAILURE() << id;
    return {};
}

Facts factsOnTheCore()
{
    Facts facts;
    facts.network = { fixtureTruth(), { "192.168.8.10", "192.168.9.10" } };
    return facts;
}
}

TEST (Network, TheTruthNamesTheHostsAndTheTwoNetworks)
{
    const auto truth = fixtureTruth();
    EXPECT_EQ (truth.hosts.at ("core"), "192.168.8.10");
    EXPECT_EQ (truth.hosts.at ("mixer"), "192.168.8.11");
    EXPECT_EQ (truth.control, "192.168.8.10/24");
    EXPECT_EQ (truth.audio, "192.168.9.10/24");
    EXPECT_TRUE (parseTruthNetwork ({}).hosts.empty()) << "no truth, no hosts";
}

TEST (Network, ASubnetHoldsItsAddresses)
{
    EXPECT_TRUE (inSubnet ("192.168.8.42", "192.168.8.10/24"));
    EXPECT_FALSE (inSubnet ("192.168.9.42", "192.168.8.10/24"));
    EXPECT_TRUE (inSubnet ("10.1.2.3", "10.0.0.0/8"));
    EXPECT_FALSE (inSubnet ("192.168.8.42", {}));
    EXPECT_FALSE (inSubnet ("not an address", "192.168.8.10/24"));
}

// The A³ networks first (control, then audio), then the rest; never loopback, link-local or a container bridge.
TEST (Network, ThisMachinesAddressesOnTheA3NetworksFirst)
{
    const std::vector<InterfaceAddress> interfaces { { "lo", "127.0.0.1" },          { "wlan0", "192.168.43.5" },
                                                     { "docker0", "172.17.0.1" },    { "br-1a2b", "172.18.0.1" },
                                                     { "veth9", "172.17.0.2" },      { "virbr0", "192.168.122.1" },
                                                     { "enp5s0", "192.168.9.10" },   { "eno1", "192.168.8.10" },
                                                     { "eno2", "169.254.10.20" } };
    EXPECT_EQ (ownAddresses (interfaces, fixtureTruth()), (std::vector<juce::String> { "192.168.8.10", "192.168.9.10", "192.168.43.5" }));
}

TEST (Network, TheMachineLine)
{
    EXPECT_EQ (machineLine ({ "192.168.8.10", "192.168.9.10" }), juce::String::fromUTF8 ("this machine · 192.168.8.10 · 192.168.9.10"));
    EXPECT_EQ (machineLine ({}), juce::String::fromUTF8 ("this machine · no network address"));
}

TEST (Hosts, TheEngineRunsOnTheTruthsCore)
{
    auto facts = factsOnTheCore();
    EXPECT_EQ (hostLine (tileOf ("core"), facts), juce::String::fromUTF8 ("local · 192.168.8.10")) << "this machine is the core";
    facts.network.own = { "192.168.8.5" };
    EXPECT_EQ (hostLine (tileOf ("core"), facts), "192.168.8.10") << "another machine is";
}

TEST (Hosts, ADeckWhereCoreHearsIt)
{
    auto facts = factsOnTheCore();
    facts.core.deckHosts = { { 1, "127.0.0.1" }, { 2, "192.168.8.30" } };
    EXPECT_EQ (hostLine (tileOf ("deck-A"), facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    EXPECT_EQ (hostLine (tileOf ("deck-B"), facts), "192.168.8.30") << "a deck on another host";
}

// Neither Core nor the truth names the host: no address, installed here or not (no fixed values,
// the maintainer, 2026-10-30: "sonst ist's kein Status").
TEST (Hosts, UnknownStaysBlankEvenWhenInstalledHere)
{
    auto facts = factsOnTheCore();
    facts.packages["stemdeck"] = { "03.0+281", "03.0+281" };
    EXPECT_EQ (hostLine (tileOf ("deck-D"), facts), "");
    facts.packages.erase ("stemdeck");
    EXPECT_EQ (hostLine (tileOf ("deck-D"), facts), "");
}

TEST (Hosts, TheDeskAndMotionWhereCoreHearsThem)
{
    auto facts = factsOnTheCore();
    facts.core.deskHost = "192.168.8.40";
    facts.core.motionHost = "192.168.8.20";
    EXPECT_EQ (hostLine (tileOf ("mixer"), facts), "192.168.8.40");
    EXPECT_EQ (hostLine (tileOf ("motion"), facts), "192.168.8.20");
}

// Core's live report comes first; where it is silent the truth names the machine, never a guess.
TEST (Hosts, TheTruthNamesWhatCoreDoesNotReport)
{
    auto facts = factsOnTheCore();
    EXPECT_EQ (hostLine (tileOf ("deck-B"), facts), "192.168.8.23");
    EXPECT_EQ (hostLine (tileOf ("deck-C"), facts), "192.168.8.20");
    EXPECT_EQ (hostLine (tileOf ("motion"), facts), "192.168.8.20");
    EXPECT_EQ (hostLine (tileOf ("deck-A"), facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    EXPECT_EQ (hostLine (tileOf ("analyzer"), facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    facts.core.deckHosts = { { 2, "192.168.8.30" } };
    EXPECT_EQ (hostLine (tileOf ("deck-B"), facts), "192.168.8.30") << "Core's report wins";
}

// The demo reads the same truth: every address in it is a file value, none is typed into the code.
TEST (Hosts, TheDemoShowsTheTruthsAddresses)
{
    const auto snapshot = demoSnapshot (catalog (4), fixtureTruth());
    EXPECT_EQ (snapshot.facts.network.own, (std::vector<juce::String> { "192.168.8.10", "192.168.9.10" }));
    EXPECT_TRUE (snapshot.facts.core.deckHosts.empty());
    EXPECT_TRUE (snapshot.facts.core.motionHost.isEmpty());
    EXPECT_EQ (hostLine (tileOf ("deck-B"), snapshot.facts), "192.168.8.23");
    EXPECT_EQ (hostLine (tileOf ("deck-C"), snapshot.facts), "192.168.8.20");
    EXPECT_EQ (hostLine (tileOf ("motion"), snapshot.facts), "192.168.8.20");
    EXPECT_EQ (hostLine (tileOf ("core"), snapshot.facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    EXPECT_EQ (hostLine (tileOf ("deck-A"), snapshot.facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    EXPECT_EQ (hostLine (tileOf ("analyzer"), snapshot.facts), juce::String::fromUTF8 ("local · 192.168.8.10"));
    EXPECT_TRUE (demoSnapshot (catalog (4), {}).facts.network.own.empty()) << "no truth, no addresses";
}
