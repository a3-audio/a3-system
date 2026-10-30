// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// One part of the system version this machine runs: a submodule of the umbrella (a3-motion's ui as
// "a3-motion/ui"), or a firmware in one ("a3-motion firmware"), with the release tag of its pinned
// commit as releaseText writes it; empty when that commit is not here (the submodule not checked out).
struct SystemRow
{
    juce::String name, tag;
};

// The umbrella checkout the installer runs from (installer/cli.py EXPECTED_REPO), read by git.
struct SystemFacts
{
    bool found = false;               // a checkout with gitlinks at all
    juce::String version;             // the umbrella's own HEAD, as releaseText writes it
    std::vector<SystemRow> rows;
    juce::String motionFirmwareTree;  // the git tree of a3-motion/firmware at the pin
    juce::String motionFirmwareTag;   // and its row's tag
};

struct Gitlink
{
    juce::String path, commit;
};

// `git ls-tree` output: the entries of mode 160000 (submodules), in git's order.
std::vector<Gitlink> parseGitlinks (const juce::String& lsTree);

// `git describe --tags --always` as a version: "v03.0" on the tag, "v03.0+413" 413 commits after it,
// the short commit when no tag precedes it.
juce::String releaseText (const juce::String& describe);

// What the A³ System card writes for a row.
juce::String systemTagText (const SystemRow& row);

// The tree the installer last flashed onto the Motion panel: install.state's [motion] firmware_tree.
juce::String flashedMotionFirmware (const juce::String& installState);
}
