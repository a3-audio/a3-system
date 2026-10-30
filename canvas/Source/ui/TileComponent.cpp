// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "TileComponent.h"

namespace canvas
{
TileComponent::TileComponent (Tile t) : tile (std::move (t))
{
    addAndMakeVisible (startStop);
    addAndMakeVisible (restart);
    startStop.onClick = [this] {
        const auto& handler = isUp() ? onStop : onStart;
        if (handler)
            handler (tile);
    };
    restart.onClick = [this] {
        if (onRestart)
            onRestart (tile);
    };
    updateButtons();
}

void TileComponent::setStatus (const TileStatus& s, const juce::String& v)
{
    status = s;
    version = v;
    updateButtons();
    repaint();
}

void TileComponent::setBusy (bool b)
{
    busy = b;
    updateButtons();
}

// Up: something of it runs or tries to, so the one key it offers is Stop.
bool TileComponent::isUp() const
{
    return status.light == Light::running || status.light == Light::starting || status.light == Light::degraded;
}

void TileComponent::updateButtons()
{
    const bool installed = status.light != Light::missing;
    startStop.setButtonText (isUp() ? "Stop" : "Start");
    startStop.setEnabled (installed && ! busy);
    restart.setEnabled (installed && ! busy && status.light != Light::stopped);
}

Metrics TileComponent::metrics() const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        return look->getMetrics();
    return {};
}

juce::Rectangle<float> TileComponent::lightArea() const
{
    const auto m = metrics();
    const auto row = getLocalBounds().toFloat().reduced (m.padding()).removeFromTop (m.header() * 1.3f);
    return row.withWidth (m.light() * 2.0f);
}

juce::Rectangle<int> TileComponent::labelArea() const
{
    const auto m = metrics();
    auto row = getLocalBounds().toFloat().reduced (m.padding()).removeFromTop (m.header() * 1.3f);
    row.removeFromLeft (m.light() * 2.0f + m.gap());
    return row.toNearestInt();
}

void TileComponent::paint (juce::Graphics& g)
{
    const auto m = metrics();
    auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel());
    if (look != nullptr)
        look->drawCard (g, getLocalBounds().toFloat());
    if (look != nullptr)
        look->drawLight (g, lightArea(), status.light);

    auto label = labelArea();
    g.setColour (status.light == Light::missing ? skin::textMuted : skin::textPrimary);
    g.setFont (juce::Font (juce::FontOptions (m.header(), juce::Font::bold)));
    g.drawFittedText (tile.label, label, juce::Justification::centredLeft, 1);

    auto text = getLocalBounds().toFloat().reduced (m.padding());
    text.removeFromTop (m.header() * 1.3f);
    const auto caption = text.removeFromTop (m.caption() * 1.5f).toNearestInt();
    g.setColour (skin::textMuted);
    g.setFont (juce::Font (juce::FontOptions (m.caption())));
    juce::String captionText = tile.caption;
    if (version.isNotEmpty())
        captionText << juce::String::fromUTF8 ("  ·  ") << version;
    if (status.updateAvailable)
        captionText << juce::String::fromUTF8 ("  ·  update");
    g.drawFittedText (captionText, caption, juce::Justification::centredLeft, 1);

    const auto line = text.removeFromTop (m.body() * 1.6f).toNearestInt();
    const bool news = status.light == Light::degraded || status.light == Light::failed;
    g.setColour (news ? lightColour (status.light) : skin::textPrimary.withAlpha (0.85f));
    g.setFont (juce::Font (juce::FontOptions (m.body())));
    g.drawFittedText (status.line, line, juce::Justification::centredLeft, 1);
}

void TileComponent::resized()
{
    const auto m = metrics();
    auto area = getLocalBounds().toFloat().reduced (m.padding());
    auto keys = area.removeFromBottom (m.key());
    const float half = (keys.getWidth() - m.gap()) * 0.5f;
    startStop.setBounds (keys.removeFromLeft (half).toNearestInt());
    keys.removeFromLeft (m.gap());
    restart.setBounds (keys.toNearestInt());
}
}
