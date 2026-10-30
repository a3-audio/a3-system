// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "GreeterComponent.h"

#include <CanvasAssets.h>

#include "ui/LinkRow.h"

namespace canvas
{
namespace
{
// The A³ System card's columns in the band and in the column.
constexpr int bandColumns = 2;
constexpr int columnColumns = 1;

int captionRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.8f); }
float systemFontHeight (const Metrics& m) { return m.caption() * 1.1f; }
int systemRow (const Metrics& m) { return juce::roundToInt (systemFontHeight (m) * 1.55f); }
int aboutRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.6f); }
int taglineRow (const Metrics& m) { return juce::roundToInt (m.title() * 1.25f); }
// The hero's text: caption, the tagline, the links and the copyright line under them.
int heroTextHeight (const Metrics& m)
{
    return captionRow (m) + taglineRow (m) + juce::roundToInt (linkHeight (m)) + aboutRow (m);
}
// The logo leads the band at four title heights, as the hero on the website leads its page.
int heroHeight (const Metrics& m) { return std::max (juce::roundToInt (m.title() * 4.0f), heroTextHeight (m)); }

float textWidth (const juce::Font& font, const juce::String& text) { return juce::GlyphArrangement::getStringWidth (font, text); }
juce::Font taglineFont (const Metrics& m) { return canvasFont (m.title(), true); }
juce::Font aboutFont (const Metrics& m) { return canvasFont (m.caption()); }

const juce::String dot = juce::String::fromUTF8 (" · ");
juce::String aboutHead() { return copyrightLine() + dot + contactAddress(); }

// One line where it fits, else a line per "·"-separated part.
juce::StringArray linesToFit (const juce::String& text, const juce::Font& font, float width)
{
    if (textWidth (font, text) <= width)
        return { text };
    auto parts = juce::StringArray::fromTokens (text, juce::String::fromUTF8 ("·"), {});
    for (auto& part : parts)
        part = part.trim();
    return parts;
}

int cardRows (int rows, int columns) { return (rows + columns - 1) / columns; }

int cardHeight (const Metrics& m, int rows, int columns)
{
    return juce::roundToInt (m.padding() * 2.0f) + captionRow (m) + cardRows (rows, columns) * systemRow (m);
}

int systemRowsOf (const SystemFacts& system) { return system.found ? static_cast<int> (system.rows.size()) : 1; }

// Under the card: the space, then the licences.
int licenceFoot (const Metrics& m, int lines) { return juce::roundToInt (m.padding()) + lines * aboutRow (m); }
}

GreeterComponent::GreeterComponent (SupportConfig supportConfig, juce::String version)
    : logo (juce::Drawable::createFromImageData (CanvasAssets::a3logo_svg, CanvasAssets::a3logo_svgSize)),
      canvasVersion (std::move (version)), support (std::move (supportConfig))
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

int GreeterComponent::bandHeight (const Metrics& m, const SupportConfig& supportConfig, int systemRows)
{
    const int cards = std::max (cardHeight (m, systemRows, bandColumns),
                                supportConfig.isEmpty() ? 0 : SupportComponent::preferredHeight (m, supportConfig));
    return heroHeight (m) + juce::roundToInt (m.gap()) + cards + licenceFoot (m, 1);
}

int GreeterComponent::systemRowCount() const
{
    return systemRowsOf (system);
}

bool GreeterComponent::setSystem (const SystemFacts& next)
{
    const auto same = [] (const SystemRow& a, const SystemRow& b) { return a.name == b.name && a.tag == b.tag; };
    if (next.found == system.found && next.version == system.version
        && std::equal (next.rows.begin(), next.rows.end(), system.rows.begin(), system.rows.end(), same))
        return false;
    const bool resize = systemRowsOf (next) != systemRowsOf (system);
    system = next;
    if (resize)
        resized();
    repaint();
    return resize;
}

juce::Rectangle<int> GreeterComponent::systemRowArea (int row) const
{
    return juce::isPositiveAndBelow (row, static_cast<int> (rowBoxes.size())) ? rowBoxes[(size_t) row] : juce::Rectangle<int>();
}

juce::StringArray GreeterComponent::aboutLines (float width) const
{
    return linesToFit (aboutHead(), aboutFont (metrics()), width);
}

juce::StringArray GreeterComponent::licenceLines (float width) const
{
    return linesToFit (licenceLine(), aboutFont (metrics()), width);
}

void GreeterComponent::layoutCard (juce::Rectangle<int> area, int columns)
{
    const auto m = metrics();
    card = area;
    auto inner = card.reduced (juce::roundToInt (m.padding()));
    cardCaption = inner.removeFromTop (captionRow (m));
    const int rows = systemRowCount();
    const int rowsPerColumn = cardRows (rows, columns);
    const int columnGap = juce::roundToInt (m.padding() * 1.5f);
    const int columnWidth = (inner.getWidth() - columnGap * (columns - 1)) / columns;
    rowBoxes.clear();
    for (int row = 0; row < rows; ++row)
    {
        const int column = row / rowsPerColumn;
        rowBoxes.push_back ({ inner.getX() + column * (columnWidth + columnGap), inner.getY() + (row % rowsPerColumn) * systemRow (m),
                              columnWidth, systemRow (m) });
    }
}

void GreeterComponent::layoutBand (juce::Rectangle<int> area)
{
    const auto m = metrics();
    const int pad = juce::roundToInt (m.padding());
    licenceBox = area.removeFromBottom (aboutRow (m));
    area.removeFromBottom (pad);

    auto hero = area.removeFromTop (heroHeight (m));
    logoBox = hero.removeFromLeft (hero.getHeight()).toFloat();
    hero.removeFromLeft (pad * 2);
    const int link = juce::roundToInt (linkHeight (m));
    auto text = hero.withSizeKeepingCentre (hero.getWidth(), heroTextHeight (m));
    captionBox = text.removeFromTop (captionRow (m));
    taglineBox = text.removeFromTop (taglineRow (m));
    layoutLinkRow (links, text.removeFromTop (link), juce::Justification::centredLeft, m);
    aboutBox = text.removeFromTop (aboutRow (m));

    // One row of cards, one height.
    area.removeFromTop (juce::roundToInt (m.gap()));
    const int cards = std::max (cardHeight (m, systemRowCount(), bandColumns),
                                support.isVisible() ? SupportComponent::preferredHeight (m, support.getConfig()) : 0);
    area.setHeight (cards);
    if (support.isVisible())
    {
        support.setBounds (area.removeFromRight (SupportComponent::preferredWidth (m, support.getConfig())));
        area.removeFromRight (juce::roundToInt (m.gap() * 1.5f));
    }
    layoutCard (area, bandColumns);
}

// The column: logo, line, links and About from the top; the cards and the licences at the foot.
void GreeterComponent::layoutColumn (juce::Rectangle<int> area)
{
    const auto m = metrics();
    const int pad = juce::roundToInt (m.padding());
    const auto width = static_cast<float> (area.getWidth());
    const int logoSide = juce::roundToInt (std::min (getWidth() * 0.5f, getHeight() * 0.25f));
    logoBox = area.removeFromTop (logoSide).withSizeKeepingCentre (logoSide, logoSide).toFloat();
    area.removeFromTop (pad * 2);
    captionBox = area.removeFromTop (captionRow (m));
    taglineBox = area.removeFromTop (taglineRow (m));
    area.removeFromTop (pad);
    // Two rows of room, should the three not fit side by side.
    const int linkRows = linkRowWidth (links, m) <= width ? 1 : 2;
    layoutLinkRow (links, area.removeFromTop (juce::roundToInt (linkHeight (m)) * linkRows), juce::Justification::centred, m);
    aboutBox = area.removeFromTop (aboutLines (width).size() * aboutRow (m));

    licenceBox = area.removeFromBottom (licenceLines (width).size() * aboutRow (m));
    area.removeFromBottom (pad);
    if (support.isVisible())
    {
        support.setBounds (area.removeFromBottom (SupportComponent::preferredHeight (m, support.getConfig())));
        area.removeFromBottom (pad);
    }
    layoutCard (area.removeFromBottom (cardHeight (m, systemRowCount(), columnColumns)), columnColumns);
}

void GreeterComponent::resized()
{
    if (isColumn())
        layoutColumn (getLocalBounds());
    else
        layoutBand (getLocalBounds());
}

// The column has room for a line per part; the band's one line is fitted where it is a little narrow.
void GreeterComponent::paintLines (juce::Graphics& g, juce::Rectangle<int> box, const juce::StringArray& lines,
                                   const juce::String& whole, const Metrics& m, juce::Justification align) const
{
    if (! isColumn())
    {
        g.drawFittedText (whole, box, align, 1, 0.85f);
        return;
    }
    for (const auto& line : lines)
        g.drawText (line, box.removeFromTop (aboutRow (m)), align, true);
}

void GreeterComponent::paintSystemCard (juce::Graphics& g, const Metrics& m) const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        look->drawCard (g, card.toFloat());
    drawCaption (g, juce::String::fromUTF8 ("A³ System"), cardCaption, m);
    g.setFont (canvasFont (systemFontHeight (m)));
    g.setColour (skin::textPrimary);
    g.drawText (system.version, cardCaption, juce::Justification::centredRight, true);

    if (! system.found)
    {
        g.setColour (skin::textMuted);
        g.drawText ("no a3-system checkout on this machine", systemRowArea (0), juce::Justification::centredLeft, true);
        return;
    }
    for (size_t i = 0; i < system.rows.size() && i < rowBoxes.size(); ++i)
    {
        const auto& row = system.rows[i];
        g.setColour (skin::textMuted);
        g.drawText (row.name, rowBoxes[i], juce::Justification::centredLeft, true);
        g.setColour (row.tag.isNotEmpty() ? skin::textPrimary : skin::textMuted);
        g.drawText (systemTagText (row), rowBoxes[i], juce::Justification::centredRight, true);
    }
}

void GreeterComponent::paint (juce::Graphics& g)
{
    const auto m = metrics();
    const auto align = isColumn() ? juce::Justification::centred : juce::Justification::centredLeft;
    g.fillAll (skin::surface);

    if (logo != nullptr)
        logo->drawWithin (g, logoBox, juce::RectanglePlacement::centred, 1.0f);

    drawCaption (g, juce::String::fromUTF8 ("A³ Canvas ") + canvasVersion, captionBox, m, align);
    g.setColour (skin::textPrimary);
    g.setFont (taglineFont (m));
    g.drawFittedText (tagline(), taglineBox, align, 1);

    g.setColour (skin::textMuted);
    g.setFont (aboutFont (m));
    paintLines (g, aboutBox, aboutLines (static_cast<float> (aboutBox.getWidth())), aboutHead(), m, align);
    paintLines (g, licenceBox, licenceLines (static_cast<float> (licenceBox.getWidth())), licenceLine(), m, align);

    paintSystemCard (g, m);
}
}
