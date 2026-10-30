// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "SupportComponent.h"

#include "ui/LinkRow.h"

namespace canvas
{
namespace
{
// The light margin a scanner needs around the code, in modules (the standard's four).
constexpr int quietModules = 4;
// The address in short lines a person can read out and compare.
constexpr int charsPerAddressLine = 14;

// Three screen pixels a module at the rig's size: what a phone camera still reads off a panel.
float qrSide (const Metrics& m) { return m.key() * 2.0f; }
int captionRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.8f); }
float addressLineHeight (const Metrics& m) { return m.caption() * 1.3f; }
juce::Font addressFont (const Metrics& m)
{
    return juce::Font (juce::FontOptions (juce::Font::getDefaultMonospacedFontName(), m.caption(), juce::Font::plain));
}
juce::Rectangle<float> copySize (const Metrics& m) { return { m.key() * 1.15f, linkHeight (m) }; }

int lineCount (const juce::String& address) { return (address.length() + charsPerAddressLine - 1) / charsPerAddressLine; }

bool hasLinks (const SupportConfig& config) { return config.kofi.isNotEmpty() || config.paypal.isNotEmpty(); }

float addressBlockHeight (const Metrics& m, const SupportConfig& config)
{
    return std::max (lineCount (config.bitcoin) * addressLineHeight (m), copySize (m).getHeight());
}

float textColumnHeight (const Metrics& m, const SupportConfig& config)
{
    float height = static_cast<float> (captionRow (m));
    if (hasLinks (config))
        height += m.gap() * 0.5f + linkHeight (m);
    if (config.bitcoin.isNotEmpty())
        height += m.gap() * 0.5f + addressBlockHeight (m, config);
    return height;
}

float textColumnWidth (const Metrics& m)
{
    const auto address = juce::GlyphArrangement::getStringWidth (addressFont (m), juce::String::repeatedString ("M", charsPerAddressLine));
    return std::max (m.key() * 3.0f, address + m.gap() + copySize (m).getWidth());
}
}

SupportComponent::SupportComponent (SupportConfig c)
    : config (std::move (c)),
      modules (config.bitcoin.isNotEmpty() ? qrModules (bitcoinUri (config.bitcoin)) : std::vector<std::vector<bool>> {})
{
    std::vector<std::pair<juce::String, juce::String>> targets;
    if (config.kofi.isNotEmpty())
        targets.push_back ({ "Ko-fi", config.kofi });
    if (config.paypal.isNotEmpty())
        targets.push_back ({ "PayPal", config.paypal });
    addLinks (*this, links, targets);

    addChildComponent (copy);
    copy.setVisible (config.bitcoin.isNotEmpty());
    copy.onClick = [this] {
        if (copyText)
            copyText (config.bitcoin);
    };
}

Metrics SupportComponent::metrics() const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        return look->getMetrics();
    return {};
}

int SupportComponent::preferredHeight (const Metrics& m, const SupportConfig& config)
{
    const float qr = config.bitcoin.isNotEmpty() ? qrSide (m) : 0.0f;
    return juce::roundToInt (m.padding() * 2.0f + std::max (qr, textColumnHeight (m, config)));
}

int SupportComponent::preferredWidth (const Metrics& m, const SupportConfig& config)
{
    const float qr = config.bitcoin.isNotEmpty() ? qrSide (m) + m.padding() : 0.0f;
    return juce::roundToInt (m.padding() * 2.0f + qr + textColumnWidth (m));
}

juce::Point<float> SupportComponent::qrModuleCentre (int x, int y) const
{
    return { qrBox.getX() + (static_cast<float> (quietModules + x) + 0.5f) * modulePixels,
             qrBox.getY() + (static_cast<float> (quietModules + y) + 0.5f) * modulePixels };
}

juce::StringArray SupportComponent::addressLines() const
{
    juce::StringArray lines;
    for (int start = 0; start < config.bitcoin.length(); start += charsPerAddressLine)
        lines.add (config.bitcoin.substring (start, start + charsPerAddressLine));
    return lines;
}

void SupportComponent::resized()
{
    const auto m = metrics();
    auto inner = getLocalBounds().reduced (juce::roundToInt (m.padding()));
    qrBox = {};
    addressBox = {};
    if (! modules.empty())
    {
        auto qrColumn = inner.removeFromLeft (juce::roundToInt (qrSide (m)));
        inner.removeFromLeft (juce::roundToInt (m.padding()));
        // Whole pixels per module, or the code blurs.
        const int count = static_cast<int> (modules.size()) + 2 * quietModules;
        modulePixels = static_cast<float> (std::max (1, std::min (qrColumn.getWidth(), qrColumn.getHeight()) / count));
        const float side = modulePixels * static_cast<float> (count);
        qrBox = qrColumn.toFloat().withSizeKeepingCentre (side, side);
        qrBox.setPosition (std::round (qrBox.getX()), std::round (qrBox.getY()));
    }

    auto column = inner.withSizeKeepingCentre (inner.getWidth(), juce::roundToInt (textColumnHeight (m, config)));
    captionBox = column.removeFromTop (captionRow (m));
    if (! links.isEmpty())
    {
        column.removeFromTop (juce::roundToInt (m.gap() * 0.5f));
        layoutLinkRow (links, column.removeFromTop (juce::roundToInt (linkHeight (m))), juce::Justification::centredLeft, m);
    }
    if (config.bitcoin.isNotEmpty())
    {
        column.removeFromTop (juce::roundToInt (m.gap() * 0.5f));
        auto block = column.removeFromTop (juce::roundToInt (addressBlockHeight (m, config)));
        const auto key = copySize (m);
        copy.setBounds (block.removeFromRight (juce::roundToInt (key.getWidth()))
                            .withSizeKeepingCentre (juce::roundToInt (key.getWidth()), juce::roundToInt (key.getHeight())));
        block.removeFromRight (juce::roundToInt (m.gap()));
        addressBox = block.withSizeKeepingCentre (block.getWidth(), juce::roundToInt (lineCount (config.bitcoin) * addressLineHeight (m)));
    }
}

void SupportComponent::paint (juce::Graphics& g)
{
    const auto m = metrics();
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        look->drawCard (g, getLocalBounds().toFloat());
    drawCaption (g, juce::String::fromUTF8 ("Support A³"), captionBox, m);

    if (! modules.empty())
    {
        // Dark modules on a light ground: the way round every scanner reads.
        g.setColour (skin::textPrimary);
        g.fillRect (qrBox);
        g.setColour (skin::background);
        for (size_t y = 0; y < modules.size(); ++y)
            for (size_t x = 0; x < modules[y].size(); ++x)
                if (modules[y][x])
                    g.fillRect (juce::Rectangle<float> (modulePixels, modulePixels)
                                    .withCentre (qrModuleCentre (static_cast<int> (x), static_cast<int> (y))));
    }

    g.setColour (skin::textPrimary);
    g.setFont (addressFont (m));
    auto line = addressBox;
    for (const auto& text : addressLines())
        g.drawText (text, line.removeFromTop (juce::roundToInt (addressLineHeight (m))), juce::Justification::centredLeft, false);
}
}
