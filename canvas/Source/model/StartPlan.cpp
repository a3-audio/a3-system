// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "StartPlan.h"

namespace canvas
{
namespace
{
const juce::String engineUnit = "a3-engine.service";
const juce::String coreUnit = "a3-core.service";
const juce::String deskBinary = "/usr/bin/a3-desk";

juce::StringArray systemctl (const juce::String& verb, const std::vector<juce::String>& units)
{
    juce::StringArray argv { "systemctl", "--user", verb };
    for (const auto& unit : units)
        argv.add (unit);
    return argv;
}

Command makeCommand (const juce::StringArray& argv, const juce::String& what)
{
    Command command;
    command.argv = argv;
    command.what = what;
    return command;
}

juce::String joined (const std::vector<juce::String>& units)
{
    juce::StringArray names;
    for (const auto& unit : units)
        names.add (unit);
    return names.joinIntoString (" ");
}

Command unitCommand (const juce::String& verb, const std::vector<juce::String>& units)
{
    return makeCommand (systemctl (verb, units), joined (units));
}

// Review Focus 2: the units open their windows on the screen the Canvas was started on.
Command importEnvironment()
{
    return makeCommand ({ "systemctl", "--user", "import-environment", "DISPLAY", "XAUTHORITY" }, "the session's screen");
}

// Plan R5: the desk has no unit of its own; it runs as a transient one.
Command runDesk (const Tile& desk, const juce::String& truthPath)
{
    juce::StringArray argv { "systemd-run", "--user", "--unit=" + desk.units.front().upToLastOccurrenceOf (".service", false, false),
                             "--collect" };
    if (truthPath.isNotEmpty())
        argv.add ("--setenv=A3_OSC_TRUTH=" + truthPath);
    argv.add (deskBinary);
    return makeCommand (argv, desk.units.front());
}

Command stopDesk (const Tile& desk)
{
    auto command = unitCommand ("stop", desk.units);
    command.mayFail = true;
    return command;
}

std::vector<Command> startCommandsOf (const Tile& tile, const juce::String& truthPath)
{
    switch (tile.kind)
    {
        case TileKind::core:
        {
            std::vector<Command> commands;
            for (const auto& unit : tile.units)
            {
                auto command = unitCommand ("start", { unit });
                // The engine and Core are waited for: what follows attaches to them.
                if (unit == engineUnit || unit == coreUnit)
                    command.waitFor = unit;
                commands.push_back (command);
            }
            return commands;
        }
        case TileKind::deck:
        {
            auto command = unitCommand ("start", tile.units);
            command.needs = engineUnit;
            return { command };
        }
        case TileKind::mixer:
            return { runDesk (tile, truthPath) };
        case TileKind::motion:
        case TileKind::analyzer:
            return { unitCommand ("start", tile.units) };
    }
    return {};
}

std::vector<Command> stopCommandsOf (const Tile& tile)
{
    switch (tile.kind)
    {
        case TileKind::core:
        {
            std::vector<Command> commands;
            for (auto unit = tile.units.rbegin(); unit != tile.units.rend(); ++unit)
                commands.push_back (unitCommand ("stop", { *unit }));
            return commands;
        }
        case TileKind::mixer:
            return { stopDesk (tile) };
        case TileKind::deck:
        case TileKind::motion:
        case TileKind::analyzer:
            return { unitCommand ("stop", tile.units) };
    }
    return {};
}

std::vector<const Tile*> tilesOfKind (const std::vector<Tile>& tiles, TileKind kind)
{
    std::vector<const Tile*> found;
    for (const auto& tile : tiles)
        if (tile.kind == kind)
            found.push_back (&tile);
    return found;
}

std::vector<juce::String> deckUnits (const std::vector<Tile>& tiles)
{
    std::vector<juce::String> units;
    for (const auto* deck : tilesOfKind (tiles, TileKind::deck))
        units.insert (units.end(), deck->units.begin(), deck->units.end());
    return units;
}

void append (std::vector<Command>& to, const std::vector<Command>& more)
{
    to.insert (to.end(), more.begin(), more.end());
}

void appendKind (std::vector<Command>& to, const std::vector<Tile>& tiles, TileKind kind,
                 const std::function<std::vector<Command> (const Tile&)>& commandsOf)
{
    for (const auto* tile : tilesOfKind (tiles, kind))
        append (to, commandsOf (*tile));
}

bool cameUp (const juce::String& unit, const UnitLookup& facts, const Waiting& waiting)
{
    for (int attempt = 0; attempt < waiting.attempts; ++attempt)
    {
        const auto state = facts (unit).active;
        if (state == "active")
            return true;
        if (state == "failed")
            return false;
        waiting.pause();
    }
    return facts (unit).active == "active";
}
}

std::vector<Command> startAll (const std::vector<Tile>& tiles, const juce::String& truthPath)
{
    const auto start = [&truthPath] (const Tile& tile) { return startCommandsOf (tile, truthPath); };
    std::vector<Command> commands { importEnvironment(), makeCommand ({ "systemctl", "--user", "daemon-reload" }, "the unit files") };
    appendKind (commands, tiles, TileKind::core, start);
    appendKind (commands, tiles, TileKind::analyzer, start);
    if (const auto decks = deckUnits (tiles); ! decks.empty())
    {
        auto command = unitCommand ("start", decks);
        command.needs = engineUnit;
        commands.push_back (command);
    }
    appendKind (commands, tiles, TileKind::mixer, start);
    appendKind (commands, tiles, TileKind::motion, start);
    return commands;
}

std::vector<Command> stopAll (const std::vector<Tile>& tiles)
{
    std::vector<Command> commands;
    appendKind (commands, tiles, TileKind::motion, stopCommandsOf);
    appendKind (commands, tiles, TileKind::mixer, stopCommandsOf);
    if (const auto decks = deckUnits (tiles); ! decks.empty())
        commands.push_back (unitCommand ("stop", decks));
    appendKind (commands, tiles, TileKind::analyzer, stopCommandsOf);
    appendKind (commands, tiles, TileKind::core, stopCommandsOf);
    return commands;
}

std::vector<Command> startTile (const Tile& tile, const juce::String& truthPath)
{
    std::vector<Command> commands { importEnvironment() };
    append (commands, startCommandsOf (tile, truthPath));
    return commands;
}

std::vector<Command> stopTile (const Tile& tile)
{
    return stopCommandsOf (tile);
}

std::vector<Command> restartTile (const Tile& tile, const juce::String& truthPath)
{
    std::vector<Command> commands { importEnvironment() };
    if (tile.kind == TileKind::mixer)
    {
        commands.push_back (stopDesk (tile));
        commands.push_back (runDesk (tile, truthPath));
        return commands;
    }
    commands.push_back (unitCommand ("restart", tile.units));
    return commands;
}

PlanResult execute (const std::vector<Command>& commands, CommandRunner& runner, const UnitLookup& facts,
                    const Waiting& waiting, const LogLine& log)
{
    const auto say = [&log] (const juce::String& line) {
        if (log)
            log (line);
    };
    PlanResult result;
    const auto fail = [&result, &say] (const Command& command, const juce::String& why) {
        result.failed.push_back (command.what);
        if (result.failedAt.isEmpty())
            result.failedAt = command.what;
        say (command.what + ": " + why);
    };
    for (const auto& command : commands)
    {
        const bool needed = command.needs.isNotEmpty()
                            && std::find (result.failed.begin(), result.failed.end(), command.needs) != result.failed.end();
        if (needed)
        {
            result.skipped.push_back (command.what);
            say (command.what + ": skipped, waiting for " + command.needs);
            continue;
        }
        say ("$ " + command.argv.joinIntoString (" "));
        const int exitCode = runner.run (command.argv, say);
        if (exitCode != 0 && ! command.mayFail)
            fail (command, "failed (exit code " + juce::String (exitCode) + ")");
        else if (exitCode == 0 && command.waitFor.isNotEmpty() && ! cameUp (command.waitFor, facts, waiting))
            fail (command, "did not come up");
    }
    return result;
}
}
