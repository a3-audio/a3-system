// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "FakeRunner.h"
#include "model/StartPlan.h"

using namespace canvas;

namespace
{
const juce::String truthPath = "/home/dj/.config/a3/laptop/a3-osc.json";

juce::StringArray linesOf (const std::vector<Command>& commands)
{
    juce::StringArray lines;
    for (const auto& command : commands)
        lines.add (command.argv.joinIntoString (" "));
    return lines;
}

int indexOf (const juce::StringArray& lines, const juce::String& fragment)
{
    for (int i = 0; i < lines.size(); ++i)
        if (lines[i].contains (fragment))
            return i;
    return -1;
}

const Tile& tileWithId (const std::vector<Tile>& tiles, const juce::String& id)
{
    for (const auto& tile : tiles)
        if (tile.id == id)
            return tile;
    throw std::out_of_range (id.toStdString());
}

// Every unit is active at once, except the ones named failed.
struct UnitTable
{
    std::set<juce::String> failed;

    UnitFacts operator() (const juce::String& unit) const
    {
        if (failed.count (unit) > 0)
            return { "loaded", "failed", "failed", "exit-code", 0 };
        return { "loaded", "active", "running", "success", 1 };
    }
};

Waiting noPause() { return { 3, [] {} }; }
}

// Review Focus 2: a Canvas started from a display manager's session hands its screen to systemd first.
TEST (StartPlan, EnvironmentIsImportedFirst)
{
    const auto lines = linesOf (startAll (catalog (4), truthPath));
    ASSERT_FALSE (lines.isEmpty());
    EXPECT_EQ (lines[0], "systemctl --user import-environment DISPLAY XAUTHORITY");
    EXPECT_EQ (lines[1], "systemctl --user daemon-reload");
}

TEST (StartPlan, EngineBeforeDecks)
{
    const auto commands = startAll (catalog (4), truthPath);
    const auto lines = linesOf (commands);
    const auto engine = indexOf (lines, "start a3-engine.service");
    const auto core = indexOf (lines, "start a3-core.service");
    const auto decks = indexOf (lines, "start stemdeck@A.service");
    ASSERT_GE (engine, 0);
    EXPECT_LT (engine, core);
    EXPECT_LT (core, decks);
    EXPECT_EQ (commands[(size_t) engine].waitFor, "a3-engine.service");
    EXPECT_EQ (commands[(size_t) core].waitFor, "a3-core.service");
    // All decks in one call.
    EXPECT_EQ (lines[decks], "systemctl --user start stemdeck@A.service stemdeck@B.service stemdeck@C.service stemdeck@D.service");
    EXPECT_EQ (commands[(size_t) decks].needs, "a3-engine.service");
}

TEST (StartPlan, TheWholeOrder)
{
    const auto lines = linesOf (startAll (catalog (2), truthPath));
    const juce::StringArray expected {
        "systemctl --user import-environment DISPLAY XAUTHORITY",
        "systemctl --user daemon-reload",
        "systemctl --user start a3-engine.service",
        "systemctl --user start a3-core.service",
        "systemctl --user start a3-core-window.service",
        "systemctl --user start beat-analyzer.service",
        "systemctl --user start stemdeck@A.service stemdeck@B.service",
        "systemd-run --user --unit=a3-desk --collect --setenv=A3_OSC_TRUTH=" + truthPath + " /usr/bin/a3-desk",
        "systemctl --user start a3-motion.service",
    };
    EXPECT_EQ (lines, expected);
}

TEST (StartPlan, StopIsTheReverse)
{
    const auto lines = linesOf (stopAll (catalog (2)));
    const juce::StringArray expected {
        "systemctl --user stop a3-motion.service",
        "systemctl --user stop a3-desk.service",
        "systemctl --user stop stemdeck@A.service stemdeck@B.service",
        "systemctl --user stop beat-analyzer.service",
        "systemctl --user stop a3-core-window.service",
        "systemctl --user stop a3-core.service",
        "systemctl --user stop a3-engine.service",
    };
    EXPECT_EQ (lines, expected);
}

TEST (StartPlan, TheDeskGetsTheLaptopTruth)
{
    const auto lines = linesOf (startTile (tileWithId (catalog (2), "mixer"), truthPath));
    EXPECT_EQ (lines.joinIntoString ("\n"),
               "systemctl --user import-environment DISPLAY XAUTHORITY\n"
               "systemd-run --user --unit=a3-desk --collect --setenv=A3_OSC_TRUTH=" + truthPath + " /usr/bin/a3-desk");
}

TEST (StartPlan, WithoutATruthPathTheDeskReadsItsOwn)
{
    const auto lines = linesOf (startTile (tileWithId (catalog (2), "mixer"), {}));
    EXPECT_EQ (lines[1], "systemd-run --user --unit=a3-desk --collect /usr/bin/a3-desk");
}

// A desk that is not running has no unit, and stopping it says so: no failure.
TEST (StartPlan, StoppingADeskThatIsNotThereIsNoFailure)
{
    const auto commands = stopTile (tileWithId (catalog (2), "mixer"));
    ASSERT_EQ (commands.size(), 1u);
    EXPECT_TRUE (commands[0].mayFail);
    FakeRunner runner;
    runner.answer ("systemctl --user stop a3-desk.service", 5);
    EXPECT_TRUE (execute (commands, runner, UnitTable {}, noPause()).ok());
}

TEST (StartPlan, OneTileStartsAndStopsAlone)
{
    const auto tiles = catalog (2);
    EXPECT_EQ (linesOf (startTile (tileWithId (tiles, "deck-B"), truthPath)).joinIntoString ("\n"),
               "systemctl --user import-environment DISPLAY XAUTHORITY\nsystemctl --user start stemdeck@B.service");
    EXPECT_EQ (linesOf (stopTile (tileWithId (tiles, "deck-B"))).joinIntoString ("\n"), "systemctl --user stop stemdeck@B.service");
    EXPECT_EQ (linesOf (startTile (tileWithId (tiles, "core"), truthPath)).joinIntoString ("\n"),
               "systemctl --user import-environment DISPLAY XAUTHORITY\n"
               "systemctl --user start a3-engine.service\n"
               "systemctl --user start a3-core.service\n"
               "systemctl --user start a3-core-window.service");
}

TEST (StartPlan, RestartIsOneCallForAUnitTile)
{
    const auto tiles = catalog (2);
    EXPECT_EQ (linesOf (restartTile (tileWithId (tiles, "motion"), truthPath)).joinIntoString ("\n"),
               "systemctl --user import-environment DISPLAY XAUTHORITY\nsystemctl --user restart a3-motion.service");
    EXPECT_EQ (linesOf (restartTile (tileWithId (tiles, "core"), truthPath)).joinIntoString ("\n"),
               "systemctl --user import-environment DISPLAY XAUTHORITY\n"
               "systemctl --user restart a3-engine.service a3-core.service a3-core-window.service");
}

TEST (StartPlan, TheDeskRestartsAsStopAndRun)
{
    const auto lines = linesOf (restartTile (tileWithId (catalog (2), "mixer"), truthPath));
    ASSERT_EQ (lines.size(), 3);
    EXPECT_EQ (lines[1], "systemctl --user stop a3-desk.service");
    EXPECT_TRUE (lines[2].startsWith ("systemd-run --user --unit=a3-desk"));
}

// Review Focus 5: the decks need the engine's ports; Core and Motion do not.
TEST (StartPlan, AFailedEngineSkipsTheDecksOnly)
{
    FakeRunner runner;
    runner.answer ("systemctl --user start a3-engine.service", 1, "Job for a3-engine.service failed.");
    const auto result = execute (startAll (catalog (2), truthPath), runner, UnitTable { { "a3-engine.service" } }, noPause());

    EXPECT_FALSE (result.ok());
    EXPECT_EQ (result.failedAt, "a3-engine.service");
    EXPECT_EQ (result.skipped, (std::vector<juce::String> { "stemdeck@A.service stemdeck@B.service" }));
    const auto ran = runner.commands();
    EXPECT_TRUE (ran.contains ("systemctl --user start a3-core.service"));
    EXPECT_TRUE (ran.contains ("systemctl --user start a3-motion.service"));
    EXPECT_FALSE (ran.contains ("systemctl --user start stemdeck@A.service stemdeck@B.service"));
}

// An engine whose start call returns 0 but which never becomes active failed just the same.
TEST (StartPlan, AnEngineThatNeverComesUpCountsAsFailed)
{
    FakeRunner runner;
    int pauses = 0;
    const auto neverActive = [] (const juce::String& unit) {
        return unit == "a3-engine.service" ? UnitFacts { "loaded", "activating", "start-pre", "success", 0 }
                                           : UnitFacts { "loaded", "active", "running", "success", 1 };
    };
    const auto result = execute (startAll (catalog (2), truthPath), runner, neverActive, { 4, [&] { ++pauses; } });
    EXPECT_EQ (result.failedAt, "a3-engine.service");
    EXPECT_EQ (pauses, 4);
    EXPECT_EQ (result.skipped.size(), 1u);
}

TEST (StartPlan, ADeckFailureDoesNotStopMotion)
{
    FakeRunner runner;
    runner.answer ("systemctl --user start stemdeck@A.service stemdeck@B.service", 1);
    const auto result = execute (startAll (catalog (2), truthPath), runner, UnitTable {}, noPause());
    EXPECT_EQ (result.failed, (std::vector<juce::String> { "stemdeck@A.service stemdeck@B.service" }));
    EXPECT_TRUE (result.skipped.empty());
    EXPECT_TRUE (runner.commands().contains ("systemctl --user start a3-motion.service"));
}

TEST (StartPlan, ExecuteReportsEveryLine)
{
    FakeRunner runner;
    runner.answer ("systemctl --user start a3-motion.service", 0, "one\ntwo");
    juce::StringArray log;
    execute (startTile (tileWithId (catalog (1), "motion"), truthPath), runner, UnitTable {}, noPause(),
             [&] (const juce::String& line) { log.add (line); });
    EXPECT_TRUE (log.contains ("$ systemctl --user start a3-motion.service"));
    EXPECT_TRUE (log.contains ("one"));
    EXPECT_TRUE (log.contains ("two"));
}
