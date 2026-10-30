// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <vector>

#include <juce_core/juce_core.h>

#include "sys/Packages.h"

namespace canvas
{
// Where "Support A³" leads. Undecided (2026-10-30): while it is empty the key is not shown, so
// nobody is sent to a placeholder. "Support", not "Donate": the UG is not a charity.
inline const juce::String supportTarget {};

// The packages the greeter names, in the rig's order; the Canvas itself follows as the last row.
const std::vector<juce::String>& greeterPackages();

// One component and what is installed of it.
struct VersionRow
{
    juce::String package, version, candidate;
    bool installed = false;
    bool updateAvailable = false;
};

// The Canvas's own version, stamped by its build (CMake's project version).
juce::String buildVersion();

// A row per greeter package from dpkg's facts ("not installed" where absent), then the Canvas from its build.
std::vector<VersionRow> versionRows (const std::map<juce::String, PackageFacts>& packages, const juce::String& canvasVersion);
// What the row says: the version, "not installed", or "installed → candidate".
juce::String versionText (const VersionRow& row);

juce::String tagline();
juce::String licenceLine();

struct Link
{
    juce::String label, url;
};

// Documentation, Website, Source; "Support A³" after them only when `support` is a web address.
std::vector<Link> greeterLinks (const juce::String& support);
}
