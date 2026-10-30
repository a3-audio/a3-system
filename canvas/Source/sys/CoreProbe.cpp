// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CoreProbe.h"

namespace canvas
{
namespace
{
juce::var objectFrom (const juce::String& body)
{
    juce::var parsed;
    if (body.isEmpty() || juce::JSON::parse (body, parsed).failed() || parsed.getDynamicObject() == nullptr)
        return {};
    return parsed;
}
}

CoreFacts parseRig (const juce::String& body)
{
    CoreFacts facts;
    const auto rig = objectFrom (body);
    if (rig.isVoid())
        return facts;
    facts.reachable = true;
    if (const auto* decks = rig["decks"].getArray())
        for (const auto& deck : *decks)
            if (static_cast<bool> (deck["present"]) && static_cast<int> (deck["deck"]) >= 1)
                facts.presentDecks.insert (static_cast<int> (deck["deck"]));
    facts.engineHeard = static_cast<bool> (rig["engine"]["heard"]);
    return facts;
}

EngineFacts parseEngineStatus (const juce::String& body)
{
    EngineFacts facts;
    const auto status = objectFrom (body);
    if (status.isVoid())
        return facts;
    facts.answers = true;
    facts.problem = status["engineProblem"].toString();
    facts.sampleRate = juce::roundToInt (static_cast<double> (status["sampleRate"]));
    facts.blockSize = static_cast<int> (status["blockSize"]);
    facts.xruns = static_cast<int> (status["xruns"]);
    facts.dspLoadPercent = static_cast<float> (static_cast<double> (status["dspLoadPercent"]));
    return facts;
}
}
