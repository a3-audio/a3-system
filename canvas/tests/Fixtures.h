// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_core/juce_core.h>

// Outputs captured on a real machine (systemctl, dpkg-query, apt-cache), or shaped after the
// code that writes them (Core's /api/rig, the engine's /api/engine/status).
inline juce::String fixture (const char* name)
{
    return juce::File (A3CANVAS_FIXTURES).getChildFile (name).loadFileAsString();
}
