// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Ini.h"

namespace canvas
{
juce::String iniValue (const juce::String& iniText, const juce::String& section, const juce::String& key)
{
    juce::String current;
    for (const auto& raw : juce::StringArray::fromLines (iniText))
    {
        const auto line = raw.trim();
        if (line.startsWithChar ('['))
        {
            current = line.fromFirstOccurrenceOf ("[", false, false).upToFirstOccurrenceOf ("]", false, false).trim();
            continue;
        }
        if (current != section || ! line.containsChar ('='))
            continue;
        if (line.upToFirstOccurrenceOf ("=", false, false).trim() == key)
            return line.fromFirstOccurrenceOf ("=", false, false).trim();
    }
    return {};
}
}
