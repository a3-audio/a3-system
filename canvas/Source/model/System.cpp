// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "System.h"

#include "model/Ini.h"

namespace canvas
{
namespace
{
bool isHex (const juce::String& text) { return text.isNotEmpty() && text.containsOnly ("0123456789abcdef"); }
bool isNumber (const juce::String& text) { return text.isNotEmpty() && text.containsOnly ("0123456789"); }
}

std::vector<Gitlink> parseGitlinks (const juce::String& lsTree)
{
    std::vector<Gitlink> links;
    for (const auto& line : juce::StringArray::fromLines (lsTree))
    {
        const auto fields = juce::StringArray::fromTokens (line.upToFirstOccurrenceOf ("\t", false, false), " ", {});
        const auto path = line.fromFirstOccurrenceOf ("\t", false, false).trim();
        if (fields.size() == 3 && fields[0] == "160000" && fields[1] == "commit" && path.isNotEmpty())
            links.push_back ({ path, fields[2] });
    }
    return links;
}

// "<tag>-<n>-g<commit>": read from the right, a tag may hold dashes of its own.
juce::String releaseText (const juce::String& describe)
{
    const auto text = describe.trim();
    const auto parts = juce::StringArray::fromTokens (text, "-", {});
    const int n = parts.size();
    if (n >= 3 && parts[n - 1].startsWithChar ('g') && isHex (parts[n - 1].substring (1)) && isNumber (parts[n - 2]))
        return juce::StringArray (parts.begin(), n - 2).joinIntoString ("-") + "+" + parts[n - 2];
    return text;
}

juce::String systemTagText (const SystemRow& row)
{
    return row.tag.isNotEmpty() ? row.tag : juce::String ("not checked out");
}

juce::String flashedMotionFirmware (const juce::String& installState)
{
    return iniValue (installState, "motion", "firmware_tree");
}
}
