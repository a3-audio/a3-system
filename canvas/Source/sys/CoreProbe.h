// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <set>

#include <juce_core/juce_core.h>

namespace canvas
{
// Core's GET /api/rig (a3-core src/a3-core/CoreView.cpp rigJson): who Core hears.
struct CoreFacts
{
    bool reachable = false;
    std::set<int> presentDecks;   // 1-based; a deck is present when Core hears its hello and the engine its audio
    bool engineHeard = false;
    std::map<int, juce::String> deckHosts;   // who sent each deck's hello; a deck never heard is absent
    juce::String deskHost;                   // the first desk Core hears
    juce::String motionHost;                 // the Motion Core follows
};

// The engine's GET /api/engine/status (a3-core app/EngineControlApi.cpp toJson).
struct EngineFacts
{
    bool answers = false;
    juce::String problem;
    int sampleRate = 0, blockSize = 0, xruns = 0;
    float dspLoadPercent = 0.0f;

    bool running() const { return answers && problem.isEmpty(); }
};

// An empty or unparsable body is "not reachable", never an error: Core may simply not run.
CoreFacts parseRig (const juce::String& body);
EngineFacts parseEngineStatus (const juce::String& body);
}
