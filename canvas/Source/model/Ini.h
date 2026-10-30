// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_core/juce_core.h>

namespace canvas
{
// The value of `key` in `[section]` of an INI text (the installer's install.conf and install.state),
// trimmed; empty when either is absent. A section given twice is read in both.
juce::String iniValue (const juce::String& iniText, const juce::String& section, const juce::String& key);
}
