// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "model/Greeter.h"

using namespace canvas;

TEST (Greeter, TheLicencesInOneLine)
{
    EXPECT_EQ (licenceLine(), juce::String::fromUTF8 (
                                  "Software GPL-3.0-or-later · Hardware CERN-OHL-S-2.0 · Documentation CC-BY-SA-4.0"));
}

TEST (Greeter, TheTaglineIsShort)
{
    EXPECT_EQ (tagline(), "Spatial DJ setup") << "the maintainer, 2026-10-30: enough without the suffix";
}

TEST (Greeter, LinksLeadToTheDocsTheWebsiteAndTheSource)
{
    const auto links = greeterLinks();
    ASSERT_EQ (links.size(), 3u);
    EXPECT_EQ (links[0].label, "Documentation");
    EXPECT_EQ (links[0].url, "https://a3-audio.github.io/a3-doc/");
    EXPECT_EQ (links[1].label, "Website");
    EXPECT_EQ (links[1].url, "https://a3-audio.github.io/");
    EXPECT_EQ (links[2].label, "Source");
    EXPECT_EQ (links[2].url, "https://github.com/a3-audio/a3-system");
}

// As the website's legal notice and footer name them.
TEST (Greeter, TheAboutLines)
{
    EXPECT_EQ (copyrightLine(), juce::String::fromUTF8 ("© 2020–2026 Raphael Eismann and contributors"));
    EXPECT_EQ (contactAddress(), "p5hcu1@systemli.org");
}

// The package build hands its version to CMake (-DA3CANVAS_VERSION); a dev build shows the project's.
TEST (Greeter, TheCanvasShowsTheVersionItsBuildWasGiven)
{
    EXPECT_EQ (buildVersion(), A3CANVAS_EXPECTED_VERSION);
}
