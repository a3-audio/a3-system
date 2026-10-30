// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "SystemRepo.h"

namespace canvas
{
namespace
{
// Where each device's firmware lives in its repository (a3-motion README, a3-mixer README).
struct FirmwareDir
{
    const char* submodule;
    const char* path;
};
constexpr FirmwareDir firmwareDirs[] { { "a3-mixer", "hardware/mainboard/firmware" }, { "a3-motion", "firmware" } };
const juce::String motionSubmodule = "a3-motion";

// The output of a git command that succeeded; nothing when it failed (its complaint is no answer).
juce::String gitOutput (CommandRunner& runner, const juce::File& dir, const juce::StringArray& args)
{
    juce::StringArray argv { "git", "-C", dir.getFullPathName() };
    argv.addArray (args);
    juce::StringArray lines;
    const int exit = runner.run (argv, [&lines] (const juce::String& text) { lines.add (text); });
    return exit == 0 ? lines.joinIntoString ("\n").trim() : juce::String();
}

juce::String tagOf (CommandRunner& runner, const juce::File& dir, const juce::String& commit)
{
    return releaseText (gitOutput (runner, dir, { "describe", "--tags", "--match", "v*", "--always", commit }));
}

const FirmwareDir* firmwareOf (const juce::String& submodule)
{
    for (const auto& dir : firmwareDirs)
        if (submodule == dir.submodule)
            return &dir;
    return nullptr;
}

// A submodule's row, then its firmware's, then its own submodules' (one level: a3-motion's ui).
void addSubmodule (CommandRunner& runner, const juce::File& repo, const Gitlink& link, SystemFacts& system)
{
    const auto dir = repo.getChildFile (link.path);
    system.rows.push_back ({ link.path, tagOf (runner, dir, link.commit) });
    if (system.rows.back().tag.isEmpty())
        return;   // not checked out: nothing more to ask it

    if (const auto* firmware = firmwareOf (link.path))
    {
        const auto changed = gitOutput (runner, dir, { "log", "-1", "--format=%H", link.commit, "--", firmware->path });
        const auto tag = changed.isNotEmpty() ? tagOf (runner, dir, changed) : juce::String();
        system.rows.push_back ({ link.path + " firmware", tag });
        if (link.path == motionSubmodule)
        {
            system.motionFirmwareTree = gitOutput (runner, dir, { "rev-parse", link.commit + ":" + firmware->path });
            system.motionFirmwareTag = tag;
        }
    }
    for (const auto& inner : parseGitlinks (gitOutput (runner, dir, { "ls-tree", link.commit })))
        system.rows.push_back ({ link.path + "/" + inner.path, tagOf (runner, dir.getChildFile (inner.path), inner.commit) });
}
}

SystemFacts readSystem (CommandRunner& runner, const juce::File& repo)
{
    SystemFacts system;
    const auto links = parseGitlinks (gitOutput (runner, repo, { "ls-tree", "HEAD" }));
    if (links.empty())
        return system;
    system.found = true;
    system.version = releaseText (gitOutput (runner, repo, { "describe", "--tags", "--match", "v*", "--always", "HEAD" }));
    for (const auto& link : links)
        addSubmodule (runner, repo, link, system);
    return system;
}

juce::File machineRepo()
{
    return juce::File::getSpecialLocation (juce::File::userHomeDirectory).getChildFile ("a3-system");
}

juce::String machineFlashedMotionFirmware()
{
    const auto state = juce::File::getSpecialLocation (juce::File::userHomeDirectory).getChildFile (".config/a3/install.state");
    return flashedMotionFirmware (state.loadFileAsString());
}
}
