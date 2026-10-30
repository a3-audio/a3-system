// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Network.h"

namespace canvas
{
namespace
{
// Interfaces that carry no A³ traffic: containers and virtual machines.
const juce::StringArray bridgePrefixes { "docker", "br-", "veth", "virbr", "lo" };

// An IPv4 address as a number; -1 when it is not one.
juce::int64 ipv4 (const juce::String& text)
{
    const auto parts = juce::StringArray::fromTokens (text.trim(), ".", {});
    if (parts.size() != 4)
        return -1;
    juce::int64 value = 0;
    for (const auto& part : parts)
    {
        if (part.isEmpty() || ! part.containsOnly ("0123456789") || part.getIntValue() > 255)
            return -1;
        value = value * 256 + part.getIntValue();
    }
    return value;
}

bool isBridge (const juce::String& interface)
{
    for (const auto& prefix : bridgePrefixes)
        if (interface.startsWith (prefix))
            return true;
    return false;
}

bool isLinkLocal (const juce::String& address) { return inSubnet (address, "169.254.0.0/16"); }
}

TruthNetwork parseTruthNetwork (const juce::var& truth)
{
    TruthNetwork network;
    if (const auto* hosts = truth["hosts"].getDynamicObject())
        for (const auto& [name, value] : hosts->getProperties())
            network.hosts[name.toString()] = value.toString();
    network.control = truth["network"]["address"].toString();
    network.audio = truth["network"]["audio_address"].toString();
    return network;
}

bool inSubnet (const juce::String& address, const juce::String& cidr)
{
    const auto value = ipv4 (address);
    const auto base = ipv4 (cidr.upToFirstOccurrenceOf ("/", false, false));
    const auto bits = cidr.fromFirstOccurrenceOf ("/", false, false);
    if (value < 0 || base < 0 || bits.isEmpty() || ! bits.containsOnly ("0123456789") || bits.getIntValue() > 32)
        return false;
    const auto mask = bits.getIntValue() == 0 ? 0 : (0xffffffffLL << (32 - bits.getIntValue())) & 0xffffffffLL;
    return (value & mask) == (base & mask);
}

bool isLoopback (const juce::String& address)
{
    return inSubnet (address, "127.0.0.0/8");
}

std::vector<juce::String> ownAddresses (const std::vector<InterfaceAddress>& interfaces, const TruthNetwork& truth)
{
    std::vector<juce::String> control, audio, other;
    for (const auto& [interface, address] : interfaces)
    {
        if (isBridge (interface) || ipv4 (address) < 0 || isLoopback (address) || isLinkLocal (address))
            continue;
        if (inSubnet (address, truth.control))
            control.push_back (address);
        else if (inSubnet (address, truth.audio))
            audio.push_back (address);
        else
            other.push_back (address);
    }
    control.insert (control.end(), audio.begin(), audio.end());
    control.insert (control.end(), other.begin(), other.end());
    return control;
}
}
