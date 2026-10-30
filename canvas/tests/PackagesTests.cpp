// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "Fixtures.h"
#include "sys/Packages.h"

using namespace canvas;

TEST (Packages, OnlyAnInstalledStateCountsAsInstalled)
{
    const auto installed = parseDpkgQuery (fixture ("dpkg-query.txt"));
    EXPECT_EQ (installed.at ("git"), "1:2.53.0-1");
    // "rc": removed, its configuration left behind. Not installed.
    EXPECT_EQ (installed.count ("appstream"), 0u);
    EXPECT_EQ (installed.count ("stemdeck"), 0u);
}

TEST (Packages, ThePolicyGivesInstalledAndCandidate)
{
    const auto policy = parseAptPolicy (fixture ("apt-policy.txt"));
    EXPECT_EQ (policy.at ("git").installed, "1:2.53.0-1");
    EXPECT_EQ (policy.at ("git").candidate, "1:2.53.0-1");
    EXPECT_EQ (policy.at ("appstream").installed, "");
    EXPECT_EQ (policy.at ("appstream").candidate, "1.2.1-1");
}

TEST (Packages, FactsJoinDpkgAndThePolicy)
{
    const auto facts = packageFacts (parseDpkgQuery (fixture ("dpkg-query.txt")), parseAptPolicy (fixture ("apt-policy.txt")),
                                     { "git", "appstream", "stemdeck" });
    EXPECT_EQ (facts.at ("git").installed, "1:2.53.0-1");
    EXPECT_FALSE (facts.at ("git").updateAvailable());
    EXPECT_EQ (facts.at ("appstream").installed, "");
    EXPECT_EQ (facts.at ("appstream").candidate, "1.2.1-1");
    EXPECT_EQ (facts.at ("stemdeck").installed, "");
    EXPECT_EQ (facts.at ("stemdeck").candidate, "");
}

TEST (Packages, ANewerCandidateIsAnUpdate)
{
    EXPECT_TRUE ((PackageFacts { "1.0", "1.1" }).updateAvailable());
    EXPECT_FALSE ((PackageFacts { "", "1.1" }).updateAvailable());
    EXPECT_FALSE ((PackageFacts { "1.0", "" }).updateAvailable());
}

TEST (Packages, TheCommandsNameThePackages)
{
    EXPECT_EQ (dpkgQueryCommand ({ "stemdeck", "a3-desk" }).joinIntoString (" "),
               "dpkg-query -W -f=${Package}\\t${Version}\\t${db:Status-Abbrev}\\n stemdeck a3-desk");
    EXPECT_EQ (aptPolicyCommand ({ "stemdeck" }).joinIntoString (" "), "apt-cache policy stemdeck");
}
