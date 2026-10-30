// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "LookAndFeel_Canvas.h"

namespace canvas
{
juce::Colour lightColour (Light light)
{
    switch (light)
    {
        case Light::running: return skin::accent;
        case Light::starting: return skin::accent.withAlpha (skin::alphaMuted);
        case Light::degraded: return skin::warning;
        case Light::failed: return skin::danger;
        case Light::stopped:
        case Light::missing: return skin::textMuted;
    }
    return skin::textMuted;
}

LookAndFeel_Canvas::LookAndFeel_Canvas()
{
    setColourScheme ({ skin::surface, skin::background, skin::surfaceRaised, skin::textMuted.withAlpha (skin::alphaOutline),
                       skin::textPrimary, skin::accent, skin::textOnAccent, skin::surfaceRaised, skin::textPrimary });
    setColour (juce::ResizableWindow::backgroundColourId, skin::surface);
    setColour (juce::TextButton::buttonColourId, skin::textPrimary.withAlpha (skin::alphaFill));
    setColour (juce::TextButton::buttonOnColourId, skin::textPrimary.withAlpha (skin::alphaFillEmphasis));
    setColour (juce::TextButton::textColourOffId, skin::textPrimary);
    setColour (juce::TextButton::textColourOnId, skin::textPrimary);
    setColour (juce::TextEditor::backgroundColourId, skin::background);
    setColour (juce::TextEditor::textColourId, skin::textMuted);
    setColour (juce::TextEditor::highlightColourId, skin::accent.withAlpha (skin::alphaFillEmphasis));
    setColour (juce::Label::textColourId, skin::textPrimary);
    setColour (juce::ScrollBar::thumbColourId, skin::textMuted.withAlpha (skin::alphaOutline));
    setColour (juce::AlertWindow::backgroundColourId, skin::surfaceRaised);
    setColour (juce::AlertWindow::textColourId, skin::textPrimary);
    setColour (juce::AlertWindow::outlineColourId, skin::textMuted.withAlpha (skin::alphaOutline));
}

void LookAndFeel_Canvas::drawButtonBackground (juce::Graphics& g, juce::Button& button, const juce::Colour& background,
                                               bool highlighted, bool down)
{
    const auto area = button.getLocalBounds().toFloat().reduced (metrics.strokeThin() * 0.5f);
    const float radius = metrics.radiusControl();
    // Pressed lifts the face at once (E3 → E4); no fade.
    auto face = down ? skin::textPrimary.withAlpha (skin::alphaFillEmphasis) : background;
    if (highlighted && ! down)
        face = face.brighter (0.15f);
    if (! button.isEnabled())
        face = face.withMultipliedAlpha (skin::alphaDisabled);
    g.setColour (face);
    g.fillRoundedRectangle (area, radius);
    g.setColour (skin::textPrimary.withAlpha (skin::alphaOutline * (button.isEnabled() ? 1.0f : skin::alphaDisabled)));
    g.drawRoundedRectangle (area, radius, metrics.strokeThin());
}

void LookAndFeel_Canvas::drawButtonText (juce::Graphics& g, juce::TextButton& button, bool, bool)
{
    auto colour = button.findColour (button.getToggleState() ? juce::TextButton::textColourOnId : juce::TextButton::textColourOffId);
    if (! button.isEnabled())
        colour = colour.withMultipliedAlpha (skin::alphaDisabled);
    g.setColour (colour);
    g.setFont (getTextButtonFont (button, button.getHeight()));
    g.drawFittedText (button.getButtonText(), button.getLocalBounds().reduced (juce::roundToInt (metrics.gap())),
                      juce::Justification::centred, 1);
}

juce::Font LookAndFeel_Canvas::getTextButtonFont (juce::TextButton&, int)
{
    return juce::Font (juce::FontOptions (metrics.body(), juce::Font::bold));
}

void LookAndFeel_Canvas::fillTextEditorBackground (juce::Graphics& g, int width, int height, juce::TextEditor& editor)
{
    g.setColour (editor.findColour (juce::TextEditor::backgroundColourId));
    g.fillRoundedRectangle (juce::Rectangle<int> (width, height).toFloat(), metrics.radiusControl());
}

void LookAndFeel_Canvas::drawLight (juce::Graphics& g, juce::Rectangle<float> area, Light light) const
{
    const auto colour = lightColour (light);
    const auto dot = area.withSizeKeepingCentre (metrics.light(), metrics.light());
    if (light == Light::missing)
    {
        g.setColour (colour.withAlpha (skin::alphaMuted));
        g.drawEllipse (dot.reduced (metrics.strokeThin()), metrics.strokeThin() * 1.5f);
        return;
    }
    if (light == Light::stopped)
    {
        g.setColour (colour.withAlpha (skin::alphaMuted));
        g.fillEllipse (dot);
        return;
    }
    // A lit light glows a little into the card, as an LED on a faceplate.
    g.setColour (colour.withAlpha (skin::alphaOutline));
    g.fillEllipse (dot.expanded (metrics.light() * 0.45f));
    g.setColour (colour);
    g.fillEllipse (dot);
}

void LookAndFeel_Canvas::drawCard (juce::Graphics& g, juce::Rectangle<float> area) const
{
    g.setColour (skin::surfaceRaised);
    g.fillRoundedRectangle (area, metrics.radiusCard());
}
}
