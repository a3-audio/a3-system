// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// What the truth (a3-osc.json) says about the network: every machine by name, and the core's
// control and audio networks as address/prefix.
struct TruthNetwork
{
    std::map<juce::String, juce::String> hosts;
    juce::String control, audio;
};

// One IPv4 address of one of this machine's interfaces.
struct InterfaceAddress
{
    juce::String interface, address;
};

// The truth's network facts and this machine's own addresses, as the greeter and rows name them.
struct NetworkFacts
{
    TruthNetwork truth;
    std::vector<juce::String> own;
};

TruthNetwork parseTruthNetwork (const juce::var& truth);
bool inSubnet (const juce::String& address, const juce::String& cidr);
bool isLoopback (const juce::String& address);

// This machine's addresses: on the control network, then the audio network, then any other;
// never loopback, link-local (169.254/16) or a container or VM bridge.
std::vector<juce::String> ownAddresses (const std::vector<InterfaceAddress>& interfaces, const TruthNetwork& truth);
juce::String machineLine (const std::vector<juce::String>& own);
}
