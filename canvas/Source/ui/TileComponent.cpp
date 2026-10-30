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

namespace
{
float keyWidth (const Metrics& m) { return TileComponent::rowKey (m) * 2.1f; }
float versionWidth (const Metrics& m) { return m.key() * 2.0f; }
float nameHeight (const Metrics& m) { return m.header() * 1.25f; }
float lineHeight (const Metrics& m) { return m.caption() * 1.45f; }
}

float TileComponent::rowHeight (const Metrics& m)
{
    return rowKey (m) + m.gap();
}

juce::Rectangle<float> TileComponent::lightArea() const
{
    const auto m = metrics();
    return getLocalBounds().toFloat().withTrimmedLeft (m.padding()).withWidth (m.light() * 2.0f);
}

juce::Rectangle<int> TileComponent::versionArea() const
{
    const auto m = metrics();
    auto area = getLocalBounds().toFloat().reduced (m.padding(), 0.0f);
    area.removeFromRight (keyWidth (m) * 2.0f + m.gap() * 2.0f);
    return area.removeFromRight (versionWidth (m)).toNearestInt();
}

juce::Rectangle<float> TileComponent::textBlock() const
{
    const auto m = metrics();
    auto area = getLocalBounds().toFloat();
    area.setLeft (lightArea().getRight() + m.gap());
    area.setRight (static_cast<float> (versionArea().getX()) - m.gap());
    return area.withSizeKeepingCentre (area.getWidth(), nameHeight (m) + lineHeight (m));
}

juce::Rectangle<int> TileComponent::labelArea() const
{
    return textBlock().removeFromTop (nameHeight (metrics())).toNearestInt();
}

void TileComponent::paint (juce::Graphics& g)
{
    const auto m = metrics();
    auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel());
    if (look != nullptr)
    {
        look->drawCard (g, getLocalBounds().toFloat());
        look->drawLight (g, lightArea(), status.light);
    }

    auto block = textBlock();
    auto name = block.removeFromTop (nameHeight (m));
    const auto nameFont = canvasFont (m.header(), true);
    g.setColour (status.light == Light::missing ? skin::textMuted : skin::textPrimary);
    g.setFont (nameFont);
    g.drawText (tile.label, name, juce::Justification::centredLeft, true);
    name.removeFromLeft (juce::GlyphArrangement::getStringWidth (nameFont, tile.label) + m.gap());
    g.setColour (skin::textMuted);
    g.setFont (canvasFont (m.caption()));
    g.drawText (tile.caption, name, juce::Justification::centredLeft, true);

    const bool news = status.light == Light::degraded || status.light == Light::failed;
    g.setColour (news ? lightColour (status.light) : skin::textPrimary.withAlpha (0.85f));
    g.drawText (status.line, block, juce::Justification::centredLeft, true);

    juce::String versionText = version;
    if (status.updateAvailable)
        versionText << juce::String::fromUTF8 ("  ·  update");
    g.setColour (status.updateAvailable ? skin::accent : skin::textMuted);
    g.drawText (versionText, versionArea(), juce::Justification::centredRight, true);
}

void TileComponent::resized()
{
    const auto m = metrics();
    auto keys = getLocalBounds().toFloat().reduced (m.padding(), 0.0f);
    keys = keys.removeFromRight (keyWidth (m) * 2.0f + m.gap()).withSizeKeepingCentre (keyWidth (m) * 2.0f + m.gap(), rowKey (m));
    restart.setBounds (keys.removeFromRight (keyWidth (m)).toNearestInt());
    keys.removeFromRight (m.gap());
    startStop.setBounds (keys.toNearestInt());
}
}
