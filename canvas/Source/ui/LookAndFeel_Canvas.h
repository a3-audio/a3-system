// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/TileStatus.h"

namespace canvas
{
// The A³ look, from a3-motion-ui's default skin quiet-indigo-2.json (the key in each comment), so the
// Canvas sits beside StemDeck, the desk and Motion as one family. Dark only (designer skill).
namespace skin
{
const juce::Colour background { 7, 8, 10 };           // background
const juce::Colour surface { 12, 12, 16 };            // surface: the window's ground (E1)
const juce::Colour surfaceRaised { 20, 21, 28 };      // surfaceRaised: cards (E2)
const juce::Colour textPrimary { 228, 228, 231 };     // textPrimary
const juce::Colour textMuted { 150, 151, 166 };       // textMuted
const juce::Colour textOnAccent { 10, 10, 15 };       // textOnAccent
const juce::Colour accent { 136, 140, 221 };          // accent
const juce::Colour warning { 237, 166, 29 };          // warning
const juce::Colour danger { 226, 75, 54 };            // danger

// The designer skill's alpha ladder, loudness by name.
constexpr float alphaFill = 0.06f;
constexpr float alphaOutline = 0.15f;
constexpr float alphaFillEmphasis = 0.28f;
constexpr float alphaDisabled = 0.35f;
constexpr float alphaMuted = 0.5f;
}

// Every size the Canvas draws, as a share of the window: the rig's screen is 768 × 1024, so at that
// size these are the skin's own sizes (fontHeader 14.06, fontBody 13.75).
struct Metrics
{
    float unit = 1.0f;   // window width / 768

    static Metrics forWidth (int width) { return { static_cast<float> (width) / 768.0f }; }
    // The rig's page fitted into a window of any shape: a laptop's 1920 × 1080 is the rig's sizes
    // scaled by its height, not two and a half times them by its width.
    static Metrics forSize (int width, int height)
    {
        return { std::min (static_cast<float> (width) / 768.0f, static_cast<float> (height) / 1024.0f) };
    }

    float title() const { return 26.0f * unit; }
    float header() const { return 19.0f * unit; }
    float body() const { return 14.5f * unit; }
    float caption() const { return 12.0f * unit; }
    float padding() const { return 14.0f * unit; }
    float gap() const { return 8.0f * unit; }
    float radiusCard() const { return 10.0f * unit; }
    float radiusControl() const { return radiusCard() - padding() * 0.4f; }
    float strokeThin() const { return std::max (1.0f, 1.0f * unit); }
    float light() const { return 12.0f * unit; }
    // A key mid-set is at least 9 mm on the rig's panel (designer: ≈ 63 px at 768 wide).
    float key() const { return 56.0f * unit; }
};

juce::Colour lightColour (Light light);

juce::Font canvasFont (float height, bool bold = false);
// Captions are upper case and tracked, as on every A³ page (designer skill).
void drawCaption (juce::Graphics&, const juce::String& text, juce::Rectangle<int> area, const Metrics&,
                  juce::Justification justification = juce::Justification::centredLeft);

class LookAndFeel_Canvas : public juce::LookAndFeel_V4
{
public:
    LookAndFeel_Canvas();

    void setMetrics (Metrics m) { metrics = m; }
    const Metrics& getMetrics() const { return metrics; }

    void drawButtonBackground (juce::Graphics&, juce::Button&, const juce::Colour& background,
                               bool highlighted, bool down) override;
    void drawButtonText (juce::Graphics&, juce::TextButton&, bool highlighted, bool down) override;
    juce::Font getTextButtonFont (juce::TextButton&, int buttonHeight) override;
    void fillTextEditorBackground (juce::Graphics&, int width, int height, juce::TextEditor&) override;
    void drawTextEditorOutline (juce::Graphics&, int, int, juce::TextEditor&) override {}

    // A light: filled when something runs or is wrong, a ring when there is nothing (missing).
    void drawLight (juce::Graphics&, juce::Rectangle<float> area, Light) const;
    void drawCard (juce::Graphics&, juce::Rectangle<float> area) const;

private:
    Metrics metrics;
};
}
