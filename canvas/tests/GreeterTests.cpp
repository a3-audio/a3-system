// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "model/Greeter.h"

using namespace canvas;

namespace
{
const juce::String canvasBuild = "0.1.0";

const VersionRow& rowFor (const std::vector<VersionRow>& rows, const juce::String& package)
{
    for (const auto& row : rows)
        if (row.package == package)
            return row;
    static const VersionRow none;
    ADD_FAILURE() << "no row for " << package;
    return none;
}
}

TEST (Greeter, OneRowPerComponentInTheRigsOrderAndTheCanvasLast)
{
    const auto rows = versionRows ({}, canvasBuild);
    std::vector<juce::String> packages;
    for (const auto& row : rows)
        packages.push_back (row.package);
    const std::vector<juce::String> expected { "a3-core-app", "stemdeck", "a3-desk", "a3-motion-ui", "beat-analyzer", "a3-canvas" };
    EXPECT_EQ (packages, expected);
}

TEST (Greeter, AnInstalledPackageShowsItsVersion)
{
    const auto rows = versionRows ({ { "a3-desk", { "03.0+120", "03.0+120" } } }, canvasBuild);
    const auto& desk = rowFor (rows, "a3-desk");
    EXPECT_TRUE (desk.installed);
    EXPECT_EQ (versionText (desk), "03.0+120");
}

TEST (Greeter, AMissingPackageSaysNotInstalled)
{
    const auto rows = versionRows ({ { "a3-desk", { {}, "03.0+120" } } }, canvasBuild);
    EXPECT_FALSE (rowFor (rows, "a3-desk").installed) << "known to apt, not installed";
    EXPECT_EQ (versionText (rowFor (rows, "a3-desk")), "not installed");
    EXPECT_EQ (versionText (rowFor (rows, "stemdeck")), "not installed") << "absent from the facts";
}

TEST (Greeter, ANewerCandidateIsShownBesideTheInstalledVersion)
{
    const auto rows = versionRows ({ { "stemdeck", { "03.0+281", "03.0+290" } } }, canvasBuild);
    const auto& deck = rowFor (rows, "stemdeck");
    EXPECT_TRUE (deck.updateAvailable);
    EXPECT_EQ (versionText (deck), juce::String::fromUTF8 ("03.0+281 → 03.0+290"));
}

TEST (Greeter, TheCanvasVersionIsItsOwnBuildNotDpkgs)
{
    const auto rows = versionRows ({ { "a3-canvas", { "03.0+5", "03.0+5" } } }, canvasBuild);
    const auto& canvasRow = rowFor (rows, "a3-canvas");
    EXPECT_TRUE (canvasRow.installed) << "it is running";
    EXPECT_EQ (versionText (canvasRow), canvasBuild);
    EXPECT_FALSE (buildVersion().isEmpty()) << "the build stamps one";
}

TEST (Greeter, TheLicencesInOneLine)
{
    EXPECT_EQ (licenceLine(), juce::String::fromUTF8 (
                                  "Software GPL-3.0-or-later · Hardware CERN-OHL-S-2.0 · Documentation CC-BY-SA-4.0"));
}

TEST (Greeter, TheTaglineIsTheWebsites)
{
    EXPECT_EQ (tagline(), juce::String::fromUTF8 ("Spatial DJ setup — 3D audio for the booth"));
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
    const auto rows = versionRows ({}, buildVersion());
    EXPECT_EQ (versionText (rows.back()), A3CANVAS_EXPECTED_VERSION);
}
