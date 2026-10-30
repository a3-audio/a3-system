// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Packages.h"

namespace canvas
{
namespace
{
juce::String versionOrEmpty (const juce::String& value)
{
    return value == "(none)" ? juce::String() : value;
}
}

juce::StringArray dpkgQueryCommand (const std::vector<juce::String>& packages)
{
    // dpkg-query expands \t and \n in its format itself; no shell is involved.
    juce::StringArray argv { "dpkg-query", "-W", "-f=${Package}\\t${Version}\\t${db:Status-Abbrev}\\n" };
    for (const auto& package : packages)
        argv.add (package);
    return argv;
}

juce::StringArray aptPolicyCommand (const std::vector<juce::String>& packages)
{
    juce::StringArray argv { "apt-cache", "policy" };
    for (const auto& package : packages)
        argv.add (package);
    return argv;
}

std::map<juce::String, juce::String> parseDpkgQuery (const juce::String& text)
{
    std::map<juce::String, juce::String> installed;
    for (const auto& line : juce::StringArray::fromLines (text))
    {
        const auto fields = juce::StringArray::fromTokens (line, "\t", {});
        if (fields.size() < 3)
            continue;
        // db:Status-Abbrev: desired, status, error. Status "i" is installed; "c" (config-files) is not.
        const auto abbrev = fields[2];
        if (abbrev.length() >= 2 && abbrev[1] == 'i')
            installed[fields[0].trim()] = fields[1].trim();
    }
    return installed;
}

std::map<juce::String, PackageFacts> parseAptPolicy (const juce::String& text)
{
    std::map<juce::String, PackageFacts> policy;
    juce::String current;
    for (const auto& line : juce::StringArray::fromLines (text))
    {
        if (line.isNotEmpty() && ! juce::CharacterFunctions::isWhitespace (line[0]) && line.trimEnd().endsWithChar (':'))
        {
            current = line.trimEnd().dropLastCharacters (1);
            policy[current];
            continue;
        }
        if (current.isEmpty())
            continue;
        const auto trimmed = line.trim();
        if (trimmed.startsWith ("Installed:"))
            policy[current].installed = versionOrEmpty (trimmed.fromFirstOccurrenceOf (":", false, false).trim());
        else if (trimmed.startsWith ("Candidate:"))
            policy[current].candidate = versionOrEmpty (trimmed.fromFirstOccurrenceOf (":", false, false).trim());
    }
    return policy;
}

std::map<juce::String, PackageFacts> packageFacts (const std::map<juce::String, juce::String>& installed,
                                                   const std::map<juce::String, PackageFacts>& policy,
                                                   const std::vector<juce::String>& names)
{
    std::map<juce::String, PackageFacts> facts;
    for (const auto& name : names)
    {
        auto& fact = facts[name];
        if (const auto found = installed.find (name); found != installed.end())
            fact.installed = found->second;
        if (const auto found = policy.find (name); found != policy.end())
            fact.candidate = found->second.candidate;
    }
    return facts;
}
}
