// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Greeter.h"

#include <CanvasVersion.h>

namespace canvas
{
juce::String buildVersion()
{
    return A3CANVAS_VERSION;
}

juce::String tagline()
{
    return "Spatial DJ setup";
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
