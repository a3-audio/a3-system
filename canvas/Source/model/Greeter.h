// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <vector>

#include <juce_core/juce_core.h>

#include "sys/Packages.h"

namespace canvas
{
// The packages the greeter names, in the rig's order; the Canvas itself follows as the last row.
const std::vector<juce::String>& greeterPackages();

// One component and what is installed of it.
struct VersionRow
{
    juce::String package, version, candidate;
    bool installed = false;
    bool updateAvailable = false;
};

// The Canvas's own version, stamped by its build: the package's, or CMake's project version.
juce::String buildVersion();

// A row per greeter package from dpkg's facts ("not installed" where absent), then the Canvas from its build.
std::vector<VersionRow> versionRows (const std::map<juce::String, PackageFacts>& packages, const juce::String& canvasVersion);
// What the row says: the version, "not installed", or "installed → candidate".
juce::String versionText (const VersionRow& row);

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
