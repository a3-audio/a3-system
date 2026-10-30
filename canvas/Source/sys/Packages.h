// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// A package's installed version (empty: not installed) and the version apt would install.
struct PackageFacts
{
    juce::String installed, candidate;

    // apt's candidate is the installed version when nothing newer is known, so any difference is newer.
    bool updateAvailable() const { return installed.isNotEmpty() && candidate.isNotEmpty() && installed != candidate; }
};

juce::StringArray dpkgQueryCommand (const std::vector<juce::String>& packages);
juce::StringArray aptPolicyCommand (const std::vector<juce::String>& packages);

// Package → version, for installed packages only (status "i" in db:Status-Abbrev's second column).
std::map<juce::String, juce::String> parseDpkgQuery (const juce::String& text);
// Package → Installed and Candidate lines; "(none)" is empty.
std::map<juce::String, PackageFacts> parseAptPolicy (const juce::String& text);
// One entry per name: dpkg decides what is installed, the policy adds the candidate.
std::map<juce::String, PackageFacts> packageFacts (const std::map<juce::String, juce::String>& installed,
                                                   const std::map<juce::String, PackageFacts>& policy,
                                                   const std::vector<juce::String>& names);
}
