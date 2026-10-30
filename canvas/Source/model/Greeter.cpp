// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Greeter.h"

#ifndef A3CANVAS_VERSION
    #error "the build stamps A3CANVAS_VERSION (cmake/CanvasSources.cmake)"
#endif

namespace canvas
{
namespace
{
const juce::String canvasPackage = "a3-canvas";

bool isWebAddress (const juce::String& text)
{
    const auto trimmed = text.trim();
    return (trimmed.startsWith ("https://") || trimmed.startsWith ("http://")) && ! trimmed.containsAnyOf (" \t\n");
}
}

const std::vector<juce::String>& greeterPackages()
{
    static const std::vector<juce::String> packages { "a3-core-app", "stemdeck", "a3-desk", "a3-motion-ui", "beat-analyzer" };
    return packages;
}

juce::String buildVersion()
{
    return A3CANVAS_VERSION;
}

std::vector<VersionRow> versionRows (const std::map<juce::String, PackageFacts>& packages, const juce::String& canvasVersion)
{
    std::vector<VersionRow> rows;
    for (const auto& name : greeterPackages())
    {
        VersionRow row;
        row.package = name;
        if (const auto found = packages.find (name); found != packages.end())
        {
            row.version = found->second.installed;
            row.candidate = found->second.candidate;
            row.installed = row.version.isNotEmpty();
            row.updateAvailable = found->second.updateAvailable();
        }
        rows.push_back (row);
    }
    rows.push_back ({ canvasPackage, canvasVersion, {}, true, false });
    return rows;
}

juce::String versionText (const VersionRow& row)
{
    if (! row.installed)
        return "not installed";
    if (row.updateAvailable)
        return row.version + juce::String::fromUTF8 (" → ") + row.candidate;
    return row.version;
}

juce::String tagline()
{
    return juce::String::fromUTF8 ("Spatial DJ setup — 3D audio for the booth");
}

// As LICENSES/ in a3-core, a3-mixer, a3-motion and a3-doc have it.
juce::String licenceLine()
{
    return juce::String::fromUTF8 ("Software GPL-3.0-or-later · Hardware CERN-OHL-S-2.0 · Documentation CC-BY-SA-4.0");
}

std::vector<Link> greeterLinks (const juce::String& support)
{
    std::vector<Link> links { { "Documentation", "https://a3-audio.github.io/a3-doc/" },
                              { "Website", "https://a3-audio.github.io/" },
                              { "Source", "https://github.com/a3-audio/a3-system" } };
    if (isWebAddress (support))
        links.push_back ({ juce::String::fromUTF8 ("Support A³"), support.trim() });
    return links;
}
}
