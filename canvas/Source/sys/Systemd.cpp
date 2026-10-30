// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Systemd.h"

namespace canvas
{
namespace
{
void addProperty (UnitFacts& unit, juce::String& id, const juce::String& key, const juce::String& value)
{
    if (key == "Id")
        id = value;
    else if (key == "LoadState")
        unit.load = value;
    else if (key == "ActiveState")
        unit.active = value;
    else if (key == "SubState")
        unit.sub = value;
    else if (key == "Result")
        unit.result = value;
    else if (key == "MainPID")
        unit.mainPid = value.getIntValue();
}
}

juce::StringArray showCommand (const std::vector<juce::String>& units)
{
    juce::StringArray argv { "systemctl", "--user", "show", "-p", "Id,LoadState,ActiveState,SubState,Result,MainPID" };
    for (const auto& unit : units)
        argv.add (unit);
    return argv;
}

std::map<juce::String, UnitFacts> parseSystemctlShow (const juce::String& text)
{
    std::map<juce::String, UnitFacts> units;
    UnitFacts unit;
    juce::String id;
    const auto finishBlock = [&] {
        if (id.isNotEmpty())
            units[id] = unit;
        unit = {};
        id = {};
    };
    for (const auto& raw : juce::StringArray::fromLines (text))
    {
        const auto line = raw.trim();
        if (line.isEmpty())
        {
            finishBlock();
            continue;
        }
        if (line.containsChar ('='))
            addProperty (unit, id, line.upToFirstOccurrenceOf ("=", false, false),
                         line.fromFirstOccurrenceOf ("=", false, false));
    }
    finishBlock();
    return units;
}
}
