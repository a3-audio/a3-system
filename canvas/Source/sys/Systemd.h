// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// What `systemctl --user show` says about one unit.
struct UnitFacts
{
    juce::String load, active, sub, result;
    int mainPid = 0;
};

// The properties Canvas reads, for the given units, as one call.
juce::StringArray showCommand (const std::vector<juce::String>& units);

// Blocks split on blank lines, each named by its Id=. A block without an Id is dropped.
std::map<juce::String, UnitFacts> parseSystemctlShow (const juce::String& text);
}
