// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/System.h"
#include "sys/CommandRunner.h"

namespace canvas
{
// The umbrella checkout at `repo` by git: its HEAD's tag, each gitlink's pinned commit described in
// its submodule, a3-motion's own submodules, and the firmware of a3-motion and a3-mixer as the tag of
// the last commit that changed it. Reads only; a submodule that is not checked out has no tag.
SystemFacts readSystem (CommandRunner& runner, const juce::File& repo);

// ~/a3-system, where the installer keeps it.
juce::File machineRepo();
// ~/.config/a3/install.state's flashed Motion firmware, or empty.
juce::String machineFlashedMotionFirmware();
}
