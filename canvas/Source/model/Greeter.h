// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// The Canvas's own version, stamped by its build: the package's, or CMake's project version.
juce::String buildVersion();

juce::String tagline();
juce::String licenceLine();
juce::String copyrightLine();
juce::String contactAddress();

struct Link
{
    juce::String label, url;
};

// Documentation, Website, Source.
std::vector<Link> greeterLinks();
}
