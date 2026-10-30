// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Greeter.h"
#include "ui/LookAndFeel_Canvas.h"
#include "ui/SupportComponent.h"

namespace canvas
{
// The Canvas's welcome: the website's logo and line, the links out, under the logo the About block
// (copyright, contact, licences), then a card with each component's version and, when anything is
// set, the Support A³ card. Wider than tall it is a band across the top of the rig's portrait page;
// taller than wide, a column beside the rig on a landscape screen.
// The versions card also says when apt has a newer one; Install and Update keys come with the
// installer interface (plan Tasks 17 and 22).
class GreeterComponent : public juce::Component
{
public:
    explicit GreeterComponent (SupportConfig support = {}, juce::String canvasVersion = buildVersion());

    void setPackages (const std::map<juce::String, PackageFacts>& packages);
    // "this machine · 192.168.8.10 · …", muted under the links.
    void setMachineLine (const juce::String& line);
    const juce::String& getMachineLine() const { return machineText; }

    // The height the band needs (the portrait page asks before it lays out the rig).
    static int bandHeight (const Metrics& m, const SupportConfig& support);

    juce::OwnedArray<juce::HyperlinkButton>& getLinks() { return links; }
    SupportComponent& supportCard() { return support; }
    juce::Rectangle<float> logoArea() const { return logoBox; }
    juce::Rectangle<int> taglineArea() const { return taglineBox; }
    juce::Rectangle<int> aboutArea() const { return aboutBox; }
    juce::Rectangle<int> machineLineArea() const { return machineBox; }
    juce::Rectangle<int> licenceArea() const { return licenceBox; }
    juce::Rectangle<int> versionsArea() const { return card; }
    juce::Rectangle<int> versionRowArea (int row) const;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    bool isColumn() const { return getHeight() > getWidth(); }
    void layoutBand (juce::Rectangle<int> area);
    void layoutColumn (juce::Rectangle<int> area);
    void layoutAbout (juce::Rectangle<int> area);
    void layoutCard (juce::Rectangle<int> area, int columns);
    juce::StringArray taglineLines (float width) const;
    juce::StringArray aboutLines (float width) const;

    std::unique_ptr<juce::Drawable> logo;
    const juce::String canvasVersion;
    juce::String machineText;
    std::vector<VersionRow> rows;
    juce::OwnedArray<juce::HyperlinkButton> links;
    SupportComponent support;

    juce::Rectangle<float> logoBox;
    juce::Rectangle<int> captionBox, taglineBox, machineBox, aboutBox, licenceBox, card, cardCaption;
    std::vector<juce::Rectangle<int>> rowBoxes;
};
}
