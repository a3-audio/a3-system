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
        {
            const int number = static_cast<int> (deck["deck"]);
            if (number < 1)
                continue;
            if (static_cast<bool> (deck["present"]))
                facts.presentDecks.insert (number);
            if (deck["host"].isString() && deck["host"].toString().isNotEmpty())
                facts.deckHosts[number] = deck["host"].toString();
        }
    if (const auto* desks = rig["desks"].getArray())
        for (const auto& desk : *desks)
            if (desk["kind"].toString() == "desk" && desk["host"].isString())
            {
                facts.deskHost = desk["host"].toString();
                break;
            }
    if (rig["motion"]["followed"].isString())
        facts.motionHost = rig["motion"]["followed"].toString();
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
