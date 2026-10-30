// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Greeter.h"

#include <CanvasVersion.h>

namespace canvas
{
namespace
{
const juce::String canvasPackage = "a3-canvas";
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

// The legal notice names the maintainer; the years are the project's (2020, as .reuse/dep5 has it).
juce::String copyrightLine()
{
    return juce::String::fromUTF8 ("© 2020–2026 Raphael Eismann and contributors");
}

// The website footer's contact.
juce::String contactAddress()
{
    return "p5hcu1@systemli.org";
}

std::vector<Link> greeterLinks()
{
    return { { "Documentation", "https://a3-audio.github.io/a3-doc/" },
             { "Website", "https://a3-audio.github.io/" },
             { "Source", "https://github.com/a3-audio/a3-system" } };
}
}
