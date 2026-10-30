// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Greeter.h"
#include "ui/LookAndFeel_Canvas.h"

namespace canvas
{
// The Canvas's welcome: the website's logo and line, the links out, and a card with the version of
// each component and the licences. Wider than tall it is a band across the top of the rig's portrait
// page; taller than wide, a column beside the rig on a laptop's landscape screen.
// The versions card also says when apt has a newer one; Install and Update keys come with the
// installer interface (plan Tasks 17 and 22).
class GreeterComponent : public juce::Component
{
public:
    explicit GreeterComponent (const juce::String& support = supportTarget, juce::String canvasVersion = buildVersion());

    void setPackages (const std::map<juce::String, PackageFacts>& packages);

    // The height the band needs (the portrait page asks before it lays out the rig).
    static int bandHeight (const Metrics& m);

    juce::OwnedArray<juce::HyperlinkButton>& getLinks() { return links; }
    juce::Rectangle<float> logoArea() const { return logoBox; }
    juce::Rectangle<int> versionsArea() const { return card; }
    juce::Rectangle<int> versionRowArea (int row) const;
    juce::Rectangle<int> licenceArea() const { return licence; }

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    bool isColumn() const { return getHeight() > getWidth(); }
    void layoutLinks (juce::Rectangle<int> area, juce::Justification justification);
    void layoutCard (juce::Rectangle<int> area, int columns);
    juce::StringArray taglineLines (float width) const;

    std::unique_ptr<juce::Drawable> logo;
    const juce::String canvasVersion;
    std::vector<VersionRow> rows;
    juce::OwnedArray<juce::HyperlinkButton> links;

    juce::Rectangle<float> logoBox;
    juce::Rectangle<int> captionBox, taglineBox, card, cardCaption, licence;
    std::vector<juce::Rectangle<int>> rowBoxes;
};
}
