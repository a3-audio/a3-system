// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "LinkRow.h"

namespace canvas
{
namespace
{
juce::Font linkFont (const Metrics& m) { return canvasFont (m.body()).withStyle (juce::Font::underlined); }

// The space after a link is part of its key, so the first one lines up with the text above it.
float linkWidth (const juce::HyperlinkButton& link, const Metrics& m)
{
    return juce::GlyphArrangement::getStringWidth (linkFont (m), link.getButtonText()) + m.padding() * 1.5f;
}
}

void addLinks (juce::Component& parent, juce::OwnedArray<juce::HyperlinkButton>& links,
               const std::vector<std::pair<juce::String, juce::String>>& labelsAndUrls)
{
    for (const auto& [label, url] : labelsAndUrls)
        parent.addAndMakeVisible (links.add (std::make_unique<juce::HyperlinkButton> (label, juce::URL (url))));
}

float linkRowWidth (const juce::OwnedArray<juce::HyperlinkButton>& links, const Metrics& m)
{
    float width = 0.0f;
    for (auto* link : links)
        width += linkWidth (*link, m);
    return width;
}

void layoutLinkRow (juce::OwnedArray<juce::HyperlinkButton>& links, juce::Rectangle<int> area,
                    juce::Justification justification, const Metrics& m)
{
    juce::FlexBox flex;
    flex.flexWrap = juce::FlexBox::Wrap::wrap;
    flex.alignContent = juce::FlexBox::AlignContent::flexStart;
    flex.justifyContent = justification == juce::Justification::centred ? juce::FlexBox::JustifyContent::center
                                                                        : juce::FlexBox::JustifyContent::flexStart;
    for (auto* link : links)
    {
        link->setFont (linkFont (m), false, justification);
        flex.items.add (juce::FlexItem (*link).withWidth (linkWidth (*link, m)).withHeight (linkHeight (m)));
    }
    flex.performLayout (area);
}
}
