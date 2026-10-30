// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "GreeterComponent.h"

#include <CanvasAssets.h>

namespace canvas
{
namespace
{
// The rows of the band (two columns) and of the column (one).
constexpr int bandColumns = 2;
constexpr int columnColumns = 1;

int rowCount() { return static_cast<int> (greeterPackages().size()) + 1; }
int captionRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.8f); }
int versionRow (const Metrics& m) { return juce::roundToInt (m.body() * 1.55f); }
int licenceRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.6f); }
int taglineRow (const Metrics& m) { return juce::roundToInt (m.title() * 1.25f); }
int linkRow (const Metrics& m) { return juce::roundToInt (m.key() * 0.6f); }
// The logo leads the band at five title heights, as the hero on the website leads its page.
int heroHeight (const Metrics& m) { return juce::roundToInt (m.title() * 5.0f); }

float textWidth (const juce::Font& font, const juce::String& text)
{
    return juce::GlyphArrangement::getStringWidth (font, text);
}

juce::Font taglineFont (const Metrics& m) { return canvasFont (m.title(), true); }
juce::Font linkFont (const Metrics& m) { return canvasFont (m.body()).withStyle (juce::Font::underlined); }
juce::Font licenceFont (const Metrics& m) { return canvasFont (m.caption()); }

int licenceLines (const Metrics& m, int width) { return textWidth (licenceFont (m), licenceLine()) <= width ? 1 : 2; }

int cardHeight (const Metrics& m, int columns, int licenceLineCount)
{
    const int rowsPerColumn = (rowCount() + columns - 1) / columns;
    return juce::roundToInt (m.padding() * 2.0f + m.gap()) + captionRow (m) + rowsPerColumn * versionRow (m)
           + licenceLineCount * licenceRow (m);
}

juce::Colour versionColour (const VersionRow& row)
{
    if (! row.installed)
        return skin::textMuted;
    return row.updateAvailable ? skin::accent : skin::textPrimary;
}
}

GreeterComponent::GreeterComponent (const juce::String& support, juce::String version)
    : logo (juce::Drawable::createFromImageData (CanvasAssets::a3logo_svg, CanvasAssets::a3logo_svgSize)),
      canvasVersion (std::move (version)), rows (versionRows ({}, canvasVersion))
{
    setOpaque (true);
    for (const auto& link : greeterLinks (support))
        addAndMakeVisible (links.add (std::make_unique<juce::HyperlinkButton> (link.label, juce::URL (link.url))));
}

Metrics GreeterComponent::metrics() const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        return look->getMetrics();
    return {};
}

int GreeterComponent::bandHeight (const Metrics& m)
{
    // The band is at least the rig's 768 wide in units, where the licences fit on one line.
    return heroHeight (m) + juce::roundToInt (m.padding()) + cardHeight (m, bandColumns, 1);
}

void GreeterComponent::setPackages (const std::map<juce::String, PackageFacts>& packages)
{
    auto next = versionRows (packages, canvasVersion);
    const auto same = [] (const VersionRow& a, const VersionRow& b) {
        return a.package == b.package && a.version == b.version && a.candidate == b.candidate;
    };
    if (std::equal (next.begin(), next.end(), rows.begin(), rows.end(), same))
        return;
    rows = std::move (next);
    repaint (card);
}

juce::Rectangle<int> GreeterComponent::versionRowArea (int row) const
{
    return juce::isPositiveAndBelow (row, static_cast<int> (rowBoxes.size())) ? rowBoxes[(size_t) row] : juce::Rectangle<int>();
}

// One line where it fits, else broken after the dash, as the website breaks it.
juce::StringArray GreeterComponent::taglineLines (float width) const
{
    const auto line = tagline();
    if (textWidth (taglineFont (metrics()), line) <= width)
        return { line };
    const auto dash = juce::String::fromUTF8 ("—");
    return { line.upToFirstOccurrenceOf (dash, true, false).trim(), line.fromFirstOccurrenceOf (dash, false, false).trim() };
}

void GreeterComponent::layoutLinks (juce::Rectangle<int> area, juce::Justification justification)
{
    const auto m = metrics();
    const auto font = linkFont (m);
    juce::FlexBox flex;
    flex.flexWrap = juce::FlexBox::Wrap::wrap;
    flex.alignContent = juce::FlexBox::AlignContent::flexStart;
    flex.justifyContent = justification == juce::Justification::centred ? juce::FlexBox::JustifyContent::center
                                                                        : juce::FlexBox::JustifyContent::flexStart;
    // The space after a link is part of its key, so the first one lines up with the text above it.
    for (auto* link : links)
    {
        link->setFont (font, false, justification);
        flex.items.add (juce::FlexItem (*link)
                            .withWidth (textWidth (font, link->getButtonText()) + m.padding() * 1.5f)
                            .withHeight (static_cast<float> (linkRow (m))));
    }
    flex.performLayout (area);
}

void GreeterComponent::layoutCard (juce::Rectangle<int> area, int columns)
{
    const auto m = metrics();
    card = area;
    auto inner = card.reduced (juce::roundToInt (m.padding()));
    cardCaption = inner.removeFromTop (captionRow (m));
    licence = inner.removeFromBottom (licenceLines (m, inner.getWidth()) * licenceRow (m));
    inner.removeFromBottom (juce::roundToInt (m.gap()));

    const int rowsPerColumn = (rowCount() + columns - 1) / columns;
    const int columnGap = juce::roundToInt (m.padding() * 2.0f);
    const int columnWidth = (inner.getWidth() - columnGap * (columns - 1)) / columns;
    rowBoxes.clear();
    for (int row = 0; row < rowCount(); ++row)
    {
        const int column = row / rowsPerColumn;
        rowBoxes.push_back ({ inner.getX() + column * (columnWidth + columnGap), inner.getY() + (row % rowsPerColumn) * versionRow (m),
                              columnWidth, versionRow (m) });
    }
}

void GreeterComponent::resized()
{
    const auto m = metrics();
    const int pad = juce::roundToInt (m.padding());
    auto area = getLocalBounds();

    if (! isColumn())
    {
        auto hero = area.removeFromTop (heroHeight (m));
        logoBox = hero.removeFromLeft (hero.getHeight()).toFloat();
        hero.removeFromLeft (pad * 2);
        const int lines = taglineLines (static_cast<float> (hero.getWidth())).size();
        auto text = hero.withSizeKeepingCentre (hero.getWidth(), captionRow (m) + lines * taglineRow (m) + pad + linkRow (m));
        captionBox = text.removeFromTop (captionRow (m));
        taglineBox = text.removeFromTop (lines * taglineRow (m));
        text.removeFromTop (pad);
        layoutLinks (text, juce::Justification::centredLeft);
        area.removeFromTop (pad);
        layoutCard (area, bandColumns);
        return;
    }

    // The column: logo, line and links from the top, the card at the foot.
    const int logoSide = juce::roundToInt (std::min (getWidth() * 0.5f, getHeight() * 0.28f));
    logoBox = area.removeFromTop (logoSide).withSizeKeepingCentre (logoSide, logoSide).toFloat();
    area.removeFromTop (pad * 2);
    captionBox = area.removeFromTop (captionRow (m));
    taglineBox = area.removeFromTop (taglineLines (static_cast<float> (area.getWidth())).size() * taglineRow (m));
    area.removeFromTop (pad);
    layoutLinks (area.removeFromTop (linkRow (m) * 2), juce::Justification::centred);
    const int cardInner = area.getWidth() - pad * 2;
    layoutCard (area.removeFromBottom (cardHeight (m, columnColumns, licenceLines (m, cardInner))), columnColumns);
}

void GreeterComponent::paint (juce::Graphics& g)
{
    const auto m = metrics();
    const auto align = isColumn() ? juce::Justification::centred : juce::Justification::centredLeft;
    g.fillAll (skin::surface);

    if (logo != nullptr)
        logo->drawWithin (g, logoBox, juce::RectanglePlacement::centred, 1.0f);

    drawCaption (g, juce::String::fromUTF8 ("A³ Canvas"), captionBox, m, align);
    g.setColour (skin::textPrimary);
    g.setFont (taglineFont (m));
    auto lineBox = taglineBox;
    for (const auto& line : taglineLines (static_cast<float> (taglineBox.getWidth())))
        g.drawText (line, lineBox.removeFromTop (taglineRow (m)), align, true);

    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        look->drawCard (g, card.toFloat());
    drawCaption (g, "Versions", cardCaption, m);
    g.setFont (canvasFont (m.body()));
    for (size_t i = 0; i < rows.size() && i < rowBoxes.size(); ++i)
    {
        g.setColour (skin::textMuted);
        g.drawText (rows[i].package, rowBoxes[i], juce::Justification::centredLeft, true);
        g.setColour (versionColour (rows[i]));
        g.drawText (versionText (rows[i]), rowBoxes[i], juce::Justification::centredRight, true);
    }

    g.setColour (skin::textMuted);
    g.setFont (licenceFont (m));
    g.drawFittedText (licenceLine(), licence, juce::Justification::centredLeft, 2, 1.0f);
}
}
