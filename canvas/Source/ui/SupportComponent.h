// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Support.h"
#include "ui/LookAndFeel_Canvas.h"

namespace canvas
{
// "Support A³": a link per set target (Ko-fi, PayPal), and a bitcoin address as a QR code, as text
// and with a key that copies it. The greeter hides the card while nothing is set.
class SupportComponent : public juce::Component
{
public:
    explicit SupportComponent (SupportConfig config);

    const SupportConfig& getConfig() const { return config; }
    juce::OwnedArray<juce::HyperlinkButton>& getLinks() { return links; }
    juce::TextButton& copyButton() { return copy; }

    // The code with its quiet zone (empty without an address), and where a module's centre falls.
    juce::Rectangle<float> qrArea() const { return qrBox; }
    juce::Point<float> qrModuleCentre (int x, int y) const;
    juce::Rectangle<int> addressArea() const { return addressBox; }

    // What Copy does with the address; the system clipboard unless a test says otherwise.
    std::function<void (const juce::String&)> copyText = [] (const juce::String& text) {
        juce::SystemClipboard::copyTextToClipboard (text);
    };

    static int preferredHeight (const Metrics& m, const SupportConfig& config);
    static int preferredWidth (const Metrics& m, const SupportConfig& config);

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    juce::StringArray addressLines() const;

    const SupportConfig config;
    const std::vector<std::vector<bool>> modules;
    juce::OwnedArray<juce::HyperlinkButton> links;
    juce::TextButton copy { "Copy" };

    juce::Rectangle<float> qrBox;
    float modulePixels = 0.0f;
    juce::Rectangle<int> captionBox, addressBox;
};
}
