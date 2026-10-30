// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "model/TileStatus.h"

using namespace canvas;

namespace
{
UnitFacts unit (const char* active, const char* result = "success")
{
    return { "loaded", active, juce::String (active) == "active" ? "running" : "dead", result, 0 };
}

struct Rig
{
    std::vector<Tile> tiles = catalog (2);
    Facts facts;

    Rig()
    {
        for (const auto& tile : tiles)
        {
            facts.packages[tile.package] = { "1.0", "1.0" };
            for (const auto& name : tile.units)
                facts.units[name] = unit ("active");
        }
        facts.core.reachable = true;
        facts.core.engineHeard = true;
        facts.core.presentDecks = { 1, 2 };
        facts.engine.answers = true;
        facts.engine.sampleRate = 48000;
        facts.engine.blockSize = 256;
    }

    const Tile& tile (const juce::String& id) const
    {
        for (const auto& t : tiles)
            if (t.id == id)
                return t;
        throw std::out_of_range (id.toStdString());
    }

    TileStatus of (const juce::String& id) const { return statusOf (tile (id), facts); }
};
}

TEST (TileStatus, AllUnitsActiveIsRunning)
{
    Rig rig;
    for (const auto& tile : rig.tiles)
        EXPECT_EQ (rig.of (tile.id).light, Light::running) << tile.id;
}

TEST (TileStatus, ATileWithoutItsPackageIsMissing)
{
    Rig rig;
    rig.facts.packages["stemdeck"] = { "", "1.0" };
    EXPECT_EQ (rig.of ("deck-A").light, Light::missing);
    EXPECT_EQ (rig.of ("deck-A").line, "Not installed (stemdeck)");
    rig.facts.packages.erase ("a3-desk");
    EXPECT_EQ (rig.of ("mixer").light, Light::missing);
}

TEST (TileStatus, AFailedUnitIsNamedWithItsResult)
{
    Rig rig;
    rig.facts.units["a3-engine.service"] = unit ("failed", "exit-code");
    const auto status = rig.of ("core");
    EXPECT_EQ (status.light, Light::failed);
    EXPECT_EQ (status.line, "a3-engine failed (exit-code)");
}

TEST (TileStatus, FailedWinsOverStarting)
{
    Rig rig;
    rig.facts.units["a3-core.service"] = unit ("activating");
    rig.facts.units["a3-core-window.service"] = unit ("failed", "signal");
    EXPECT_EQ (rig.of ("core").light, Light::failed);
}

TEST (TileStatus, AnActivatingUnitIsStarting)
{
    Rig rig;
    rig.facts.units["stemdeck@B.service"] = unit ("activating");
    EXPECT_EQ (rig.of ("deck-B").light, Light::starting);
    rig.facts.units["stemdeck@B.service"] = unit ("reloading");
    EXPECT_EQ (rig.of ("deck-B").light, Light::starting);
}

TEST (TileStatus, NothingActiveIsStopped)
{
    Rig rig;
    rig.facts.units["a3-motion.service"] = unit ("inactive");
    EXPECT_EQ (rig.of ("motion").light, Light::stopped);
    EXPECT_EQ (rig.of ("motion").line, "Stopped");
}

// The desk's transient unit does not exist until the Canvas starts it (plan R5).
TEST (TileStatus, AUnitSystemdDoesNotKnowIsStopped)
{
    Rig rig;
    rig.facts.units["a3-desk.service"] = { "not-found", "inactive", "dead", "success", 0 };
    EXPECT_EQ (rig.of ("mixer").light, Light::stopped);
    rig.facts.units.erase ("a3-desk.service");
    EXPECT_EQ (rig.of ("mixer").light, Light::stopped);
}

TEST (TileStatus, SomeUnitsUpIsDegradedAndSaysWhich)
{
    Rig rig;
    rig.facts.units["a3-core-window.service"] = unit ("inactive");
    const auto status = rig.of ("core");
    EXPECT_EQ (status.light, Light::degraded);
    EXPECT_EQ (status.line, "a3-core-window not running");
}

TEST (TileStatus, ADeckCoreDoesNotHearIsDegraded)
{
    Rig rig;
    rig.facts.core.presentDecks = { 1 };
    EXPECT_EQ (rig.of ("deck-A").light, Light::running);
    EXPECT_EQ (rig.of ("deck-B").light, Light::degraded);
    EXPECT_EQ (rig.of ("deck-B").line, "Running, no audio link");
}

// Core down is the core tile's news, not every deck's.
TEST (TileStatus, AnUnreachableCoreDoesNotDegradeTheDecks)
{
    Rig rig;
    rig.facts.core = {};
    EXPECT_EQ (rig.of ("deck-A").light, Light::running);
}

TEST (TileStatus, ACoreWhoseEngineDoesNotAnswerIsDegraded)
{
    Rig rig;
    rig.facts.engine = {};
    EXPECT_EQ (rig.of ("core").light, Light::degraded);
    EXPECT_EQ (rig.of ("core").line, "Engine not answering");
}

TEST (TileStatus, AnEngineProblemIsShown)
{
    Rig rig;
    rig.facts.engine.problem = "port taken";
    EXPECT_EQ (rig.of ("core").light, Light::degraded);
    EXPECT_EQ (rig.of ("core").line, "Engine: port taken");
}

TEST (TileStatus, ARunningCoreSaysRateAndBlock)
{
    Rig rig;
    rig.facts.engine.dspLoadPercent = 11.5f;
    EXPECT_EQ (rig.of ("core").line, juce::String::fromUTF8 ("Running · 48 kHz · 256 · DSP 12 %"));
}

TEST (TileStatus, ANewerPackageIsAnUpdate)
{
    Rig rig;
    rig.facts.packages["a3-motion-ui"] = { "1.0", "1.1" };
    EXPECT_TRUE (rig.of ("motion").updateAvailable);
    EXPECT_FALSE (rig.of ("mixer").updateAvailable);
}

TEST (TileStatus, TheWindowPidIsTheWindowUnitsMainPid)
{
    Rig rig;
    rig.facts.units["stemdeck@A.service"].mainPid = 4242;
    EXPECT_EQ (rig.of ("deck-A").windowPid, 4242);
    EXPECT_EQ (rig.of ("analyzer").windowPid, 0);
}
