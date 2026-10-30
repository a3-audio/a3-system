// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <functional>

#include "model/AppCatalog.h"
#include "sys/CommandRunner.h"
#include "sys/Systemd.h"

namespace canvas
{
struct Command
{
    juce::StringArray argv;
    juce::String what;      // what it starts or stops, as the log and PlanResult name it
    juce::String waitFor;   // a unit that must become active, or empty
    juce::String needs;     // a command's `what` that must not have failed, or empty
    bool mayFail = false;   // an exit code that is no news (stopping a desk that does not run)
};

std::vector<Command> startAll (const std::vector<Tile>& tiles, const juce::String& truthPath);
std::vector<Command> stopAll (const std::vector<Tile>& tiles);
std::vector<Command> startTile (const Tile& tile, const juce::String& truthPath);
std::vector<Command> stopTile (const Tile& tile);
std::vector<Command> restartTile (const Tile& tile, const juce::String& truthPath);

// How long a waitFor is given: `attempts` looks, `pause` between them (the app: 30 × 500 ms).
struct Waiting
{
    int attempts = 30;
    std::function<void()> pause = [] { juce::Thread::sleep (500); };
};

struct PlanResult
{
    std::vector<juce::String> skipped, failed;
    juce::String failedAt;   // the first failure

    bool ok() const { return failed.empty() && skipped.empty(); }
};

using UnitLookup = std::function<UnitFacts (const juce::String& unit)>;
using LogLine = std::function<void (const juce::String&)>;

// Runs the commands in order. A failure is recorded and the rest continue, except commands that
// need what failed: those are skipped (a failed engine skips the decks, Review Focus 5).
PlanResult execute (const std::vector<Command>& commands, CommandRunner& runner, const UnitLookup& facts,
                    const Waiting& waiting = {}, const LogLine& log = {});
}
