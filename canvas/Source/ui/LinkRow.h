// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "ui/LookAndFeel_Canvas.h"

namespace canvas
{
// A link's key is a fingertip high, however small its text.
inline float linkHeight (const Metrics& m) { return m.key() * 0.6f; }

void addLinks (juce::Component& parent, juce::OwnedArray<juce::HyperlinkButton>& links,
               const std::vector<std::pair<juce::String, juce::String>>& labelsAndUrls);

// Links side by side (wrapping when the row is too narrow), each as wide as its text and a gap.
void layoutLinkRow (juce::OwnedArray<juce::HyperlinkButton>& links, juce::Rectangle<int> area,
                    juce::Justification justification, const Metrics& m);
// The width the links take in one row.
float linkRowWidth (const juce::OwnedArray<juce::HyperlinkButton>& links, const Metrics& m);
}
