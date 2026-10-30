// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "Fixtures.h"
#include "sys/Systemd.h"

using namespace canvas;

TEST (Systemd, EachBlockIsNamedByItsId)
{
    const auto units = parseSystemctlShow (fixture ("systemctl-show.txt"));
    ASSERT_EQ (units.size(), 3u);
    const auto& running = units.at ("pipewire.service");
    EXPECT_EQ (running.load, "loaded");
    EXPECT_EQ (running.active, "active");
    EXPECT_EQ (running.sub, "running");
    EXPECT_EQ (running.result, "success");
    EXPECT_EQ (running.mainPid, 650);
    EXPECT_EQ (units.at ("xdg-desktop-portal.service").active, "activating");
    EXPECT_EQ (units.at ("a3-engine.service").load, "not-found");
    EXPECT_EQ (units.at ("a3-engine.service").mainPid, 0);
}

TEST (Systemd, AFailedUnitKeepsItsResult)
{
    const auto units = parseSystemctlShow (fixture ("systemctl-show-failed.txt"));
    EXPECT_EQ (units.at ("xdg-desktop-portal.service").active, "failed");
    EXPECT_EQ (units.at ("xdg-desktop-portal.service").result, "timeout");
}

TEST (Systemd, NothingParsesToNothing)
{
    EXPECT_TRUE (parseSystemctlShow ({}).empty());
    EXPECT_TRUE (parseSystemctlShow ("garbage\n\n=\n").empty());
}

TEST (Systemd, TheShowCommandAsksExactlyTheFactsItParses)
{
    const auto argv = showCommand ({ "a3-engine.service", "stemdeck@A.service" });
    EXPECT_EQ (argv.joinIntoString (" "),
               "systemctl --user show -p Id,LoadState,ActiveState,SubState,Result,MainPID "
               "a3-engine.service stemdeck@A.service");
}
