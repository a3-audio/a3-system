// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "GreeterComponent.h"

#include <CanvasAssets.h>

#include "ui/LinkRow.h"

namespace canvas
{
namespace
{
// The versions card's columns in the band and in the column.
constexpr int bandColumns = 2;
constexpr int columnColumns = 1;

int rowCount() { return static_cast<int> (greeterPackages().size()) + 1; }
int captionRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.8f); }
float versionFontHeight (const Metrics& m) { return m.caption() * 1.1f; }
int versionRow (const Metrics& m) { return juce::roundToInt (versionFontHeight (m) * 1.55f); }
int aboutRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.6f); }
int taglineRow (const Metrics& m) { return juce::roundToInt (m.title() * 1.25f); }
// The logo leads the band at four title heights, as the hero on the website leads its page.
int heroHeight (const Metrics& m) { return juce::roundToInt (m.title() * 4.0f); }

float textWidth (const juce::Font& font, const juce::String& text) { return juce::GlyphArrangement::getStringWidth (font, text); }
juce::Font taglineFont (const Metrics& m) { return canvasFont (m.title(), true); }
juce::Font aboutFont (const Metrics& m) { return canvasFont (m.caption()); }

juce::String aboutHead() { return copyrightLine() + juce::String::fromUTF8 (" · ") + contactAddress(); }

int cardHeight (const Metrics& m, int columns)
{
    const int rowsPerColumn = (rowCount() + columns - 1) / columns;
    return juce::roundToInt (m.padding() * 2.0f) + captionRow (m) + rowsPerColumn * versionRow (m);
}

// The band: the hero, the About block's two lines, the cards.
int bandAboutHeight (const Metrics& m) { return juce::roundToInt (m.gap()) + 2 * aboutRow (m); }

juce::Colour versionColour (const VersionRow& row)
{
    if (! row.installed)
        return skin::textMuted;
    return row.updateAvailable ? skin::accent : skin::textPrimary;
}
}

GreeterComponent::GreeterComponent (SupportConfig supportConfig, juce::String version)
    : logo (juce::Drawable::createFromImageData (CanvasAssets::a3logo_svg, CanvasAssets::a3logo_svgSize)),
      canvasVersion (std::move (version)), rows (versionRows ({}, canvasVersion)), support (std::move (supportConfig))
{
    setOpaque (true);
    std::vector<std::pair<juce::String, juce::String>> targets;
    for (const auto& link : greeterLinks())
        targets.push_back ({ link.label, link.url });
    addLinks (*this, links, targets);
    addChildComponent (support);
    support.setVisible (! support.getConfig().isEmpty());
}

Metrics GreeterComponent::metrics() const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        return look->getMetrics();
    return {};
}

int GreeterComponent::bandHeight (const Metrics& m, const SupportConfig& supportConfig)
{
    const int cards = std::max (cardHeight (m, bandColumns),
                                supportConfig.isEmpty() ? 0 : SupportComponent::preferredHeight (m, supportConfig));
    return heroHeight (m) + bandAboutHeight (m) + juce::roundToInt (m.padding()) + cards;
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

// Copyright and contact on one line, the licences on the next; split where a line is too wide.
juce::StringArray GreeterComponent::aboutLines (float width) const
{
    const auto font = aboutFont (metrics());
    juce::StringArray lines;
    if (textWidth (font, aboutHead()) <= width)
        lines.add (aboutHead());
    else
        lines.addArray ({ copyrightLine(), contactAddress() });
    if (textWidth (font, licenceLine()) <= width)
        lines.add (licenceLine());
    else
        lines.addArray (juce::StringArray::fromTokens (licenceLine(), juce::String::fromUTF8 ("·"), {}));
    for (auto& line : lines)
        line = line.trim();
    return lines;
}

void GreeterComponent::layoutAbout (juce::Rectangle<int> area)
{
    const auto m = metrics();
    const auto lines = aboutLines (static_cast<float> (area.getWidth()));
    aboutBox = area.withHeight (lines.size() * aboutRow (m));
    // The licences are the last lines: those after the copyright and contact.
    const int licenceLines = lines.size() - (lines[0] == aboutHead() ? 1 : 2);
    licenceBox = aboutBox.withTrimmedTop (aboutBox.getHeight() - licenceLines * aboutRow (m));
}

void GreeterComponent::layoutCard (juce::Rectangle<int> area, int columns)
{
    const auto m = metrics();
    card = area;
    auto inner = card.reduced (juce::roundToInt (m.padding()));
    cardCaption = inner.removeFromTop (captionRow (m));
    const int rowsPerColumn = (rowCount() + columns - 1) / columns;
    const int columnGap = juce::roundToInt (m.padding() * 1.5f);
    const int columnWidth = (inner.getWidth() - columnGap * (columns - 1)) / columns;
    rowBoxes.clear();
    for (int row = 0; row < rowCount(); ++row)
    {
        const int column = row / rowsPerColumn;
        rowBoxes.push_back ({ inner.getX() + column * (columnWidth + columnGap), inner.getY() + (row % rowsPerColumn) * versionRow (m),
                              columnWidth, versionRow (m) });
    }
}

void GreeterComponent::layoutBand (juce::Rectangle<int> area)
{
    const auto m = metrics();
    const int pad = juce::roundToInt (m.padding());
    auto hero = area.removeFromTop (heroHeight (m));
    logoBox = hero.removeFromLeft (hero.getHeight()).toFloat();
    hero.removeFromLeft (pad * 2);
    const int lines = taglineLines (static_cast<float> (hero.getWidth())).size();
    const int link = juce::roundToInt (linkHeight (m));
    auto text = hero.withSizeKeepingCentre (hero.getWidth(), captionRow (m) + lines * taglineRow (m) + link);
    captionBox = text.removeFromTop (captionRow (m));
    taglineBox = text.removeFromTop (lines * taglineRow (m));
    layoutLinkRow (links, text, juce::Justification::centredLeft, m);

    // Under the logo.
    area.removeFromTop (juce::roundToInt (m.gap()));
    layoutAbout (area.removeFromTop (2 * aboutRow (m)));
    area.removeFromTop (pad);

    if (support.isVisible())
    {
        support.setBounds (area.removeFromRight (SupportComponent::preferredWidth (m, support.getConfig()))
                               .withHeight (SupportComponent::preferredHeight (m, support.getConfig())));
        area.removeFromRight (juce::roundToInt (m.gap() * 1.5f));
    }
    layoutCard (area.withHeight (std::max (cardHeight (m, bandColumns), support.isVisible() ? support.getHeight() : 0)), bandColumns);
}

// The column: logo, line, links and About from the top, the cards at the foot.
void GreeterComponent::layoutColumn (juce::Rectangle<int> area)
{
    const auto m = metrics();
    const int pad = juce::roundToInt (m.padding());
    const int logoSide = juce::roundToInt (std::min (getWidth() * 0.5f, getHeight() * 0.25f));
    logoBox = area.removeFromTop (logoSide).withSizeKeepingCentre (logoSide, logoSide).toFloat();
    area.removeFromTop (pad);
    const int aboutLineCount = aboutLines (static_cast<float> (area.getWidth())).size();
    layoutAbout (area.removeFromTop (aboutLineCount * aboutRow (m)));
    area.removeFromTop (pad * 2);
    captionBox = area.removeFromTop (captionRow (m));
    taglineBox = area.removeFromTop (taglineLines (static_cast<float> (area.getWidth())).size() * taglineRow (m));
    area.removeFromTop (pad);
    layoutLinkRow (links, area.removeFromTop (juce::roundToInt (linkHeight (m)) * 2), juce::Justification::centred, m);

    if (support.isVisible())
    {
        support.setBounds (area.removeFromBottom (SupportComponent::preferredHeight (m, support.getConfig())));
        area.removeFromBottom (pad);
    }
    layoutCard (area.removeFromBottom (cardHeight (m, columnColumns)), columnColumns);
}

void GreeterComponent::resized()
{
    if (isColumn())
        layoutColumn (getLocalBounds());
    else
        layoutBand (getLocalBounds());
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

    g.setColour (skin::textMuted);
    g.setFont (aboutFont (m));
    auto aboutLine = aboutBox;
    for (const auto& line : aboutLines (static_cast<float> (aboutBox.getWidth())))
        g.drawText (line, aboutLine.removeFromTop (aboutRow (m)), align, true);

    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        look->drawCard (g, card.toFloat());
    drawCaption (g, "Versions", cardCaption, m);
    g.setFont (canvasFont (versionFontHeight (m)));
    for (size_t i = 0; i < rows.size() && i < rowBoxes.size(); ++i)
    {
        g.setColour (skin::textMuted);
        g.drawText (rows[i].package, rowBoxes[i], juce::Justification::centredLeft, true);
        g.setColour (versionColour (rows[i]));
        g.drawText (versionText (rows[i]), rowBoxes[i], juce::Justification::centredRight, true);
    }
}
}
