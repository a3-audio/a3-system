// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Greeter.h"
#include "model/System.h"
#include "ui/LookAndFeel_Canvas.h"
#include "ui/SupportComponent.h"

namespace canvas
{
// The Canvas's welcome, about the project: the website's logo and line, the links out with copyright
// and contact under them, the A³ System card (each submodule and firmware with the release tag the
// system version pins), when anything is set the Support A³ card, and the licences at the very bottom.
// Wider than tall it is a band across the top of the rig's portrait page; taller than wide, a column
// beside the rig on a landscape screen. What runs where, and its versions, is the rig's (the rows).
class GreeterComponent : public juce::Component
{
public:
    explicit GreeterComponent (SupportConfig support = {}, juce::String canvasVersion = buildVersion());

    // True when the card's row count changed: the page lays out again.
    bool setSystem (const SystemFacts& system);
    int systemRowCount() const;

    // The height the band needs (the portrait page asks before it lays out the rig).
    static int bandHeight (const Metrics& m, const SupportConfig& support, int systemRows);

    juce::OwnedArray<juce::HyperlinkButton>& getLinks() { return links; }
    SupportComponent& supportCard() { return support; }
    juce::Rectangle<float> logoArea() const { return logoBox; }
    juce::Rectangle<int> taglineArea() const { return taglineBox; }
    // Copyright and contact.
    juce::Rectangle<int> aboutArea() const { return aboutBox; }
    juce::Rectangle<int> licenceArea() const { return licenceBox; }
    juce::Rectangle<int> systemArea() const { return card; }
    juce::Rectangle<int> systemRowArea (int row) const;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    bool isColumn() const { return getHeight() > getWidth(); }
    void layoutBand (juce::Rectangle<int> area);
    void layoutColumn (juce::Rectangle<int> area);
    void layoutCard (juce::Rectangle<int> area, int columns);
    juce::StringArray aboutLines (float width) const;
    juce::StringArray licenceLines (float width) const;
    void paintSystemCard (juce::Graphics&, const Metrics&) const;
    void paintLines (juce::Graphics&, juce::Rectangle<int> box, const juce::StringArray& lines, const juce::String& whole,
                     const Metrics&, juce::Justification) const;

    std::unique_ptr<juce::Drawable> logo;
    const juce::String canvasVersion;
    SystemFacts system;
    juce::OwnedArray<juce::HyperlinkButton> links;
    SupportComponent support;

    juce::Rectangle<float> logoBox;
    juce::Rectangle<int> captionBox, taglineBox, aboutBox, licenceBox, card, cardCaption;
    std::vector<juce::Rectangle<int>> rowBoxes;
};
}
