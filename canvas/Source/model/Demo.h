// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/AppCatalog.h"
#include "sys/CommandRunner.h"
#include "sys/StatusPoller.h"

namespace canvas
{
// `a3-canvas --demo`: a made-up rig for pictures and trying the window, wired to no unit. Everything
// runs except the last deck, which is stopped. The facts go through the same rules as a real poll.
Snapshot demoSnapshot (const std::vector<Tile>& tiles);

// Runs nothing: says what it would have run.
class DemoRunner : public CommandRunner
{
public:
    int run (const juce::StringArray& argv, const LineCallback& line) override;
};
}
