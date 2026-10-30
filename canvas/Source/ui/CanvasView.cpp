// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CanvasView.h"

namespace canvas
{
namespace
{
// Shares of the page: the header, and the band of log and packages under the tiles.
constexpr float headerShare = 0.085f;
constexpr float bottomShare = 0.2f;
constexpr int maxLogLines = 400;

juce::Font font (float height, bool bold = false)
{
    return juce::Font (juce::FontOptions (height, bold ? juce::Font::bold : juce::Font::plain));
}

// Captions are upper case and tracked, as on every A³ page (designer skill).
void drawCaption (juce::Graphics& g, const juce::String& text, juce::Rectangle<int> area, const Metrics& m)
{
    g.setColour (skin::textMuted);
    g.setFont (font (m.caption(), true).withExtraKerningFactor (0.08f));
    g.drawText (text.toUpperCase(), area, juce::Justification::centredLeft, false);
}

bool landscape (juce::Rectangle<int> area) { return area.getWidth() > area.getHeight(); }
}

void showConfirmation (const juce::String& question, const juce::String& detail, std::function<void()> then)
{
    const auto options = juce::MessageBoxOptions::makeOptionsOkCancel (juce::MessageBoxIconType::QuestionIcon, question,
                                                                       detail, "Yes", "Cancel");
    juce::AlertWindow::showAsync (options, [then] (int result) {
        if (result == 1 && then)
            then();
    });
}

// -- InstallPanel ----------------------------------------------------------------

Metrics InstallPanel::metrics() const
{
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        return look->getMetrics();
    return {};
}

void InstallPanel::setPackages (const std::map<juce::String, PackageFacts>& p)
{
    if (p.size() == packages.size()
        && std::equal (p.begin(), p.end(), packages.begin(), [] (const auto& a, const auto& b) {
               return a.first == b.first && a.second.installed == b.second.installed && a.second.candidate == b.second.candidate;
           }))
        return;
    packages = p;
    repaint();
}

void InstallPanel::paint (juce::Graphics& g)
{
    const auto m = metrics();
    if (auto* look = dynamic_cast<LookAndFeel_Canvas*> (&getLookAndFeel()))
        look->drawCard (g, getLocalBounds().toFloat());
    auto area = getLocalBounds().reduced (juce::roundToInt (m.padding()));
    drawCaption (g, "Packages", area.removeFromTop (juce::roundToInt (m.caption() * 1.8f)), m);

    const int row = juce::roundToInt (m.body() * 1.55f);
    for (const auto& [name, facts] : packages)
    {
        if (area.getHeight() < row)
            break;
        auto line = area.removeFromTop (row);
        g.setFont (font (m.body()));
        g.setColour (facts.installed.isEmpty() ? skin::textMuted : skin::textPrimary);
        g.drawText (name, line, juce::Justification::centredLeft, true);
        juce::String version = facts.installed.isEmpty() ? juce::String ("not installed") : facts.installed;
        if (facts.updateAvailable())
            version << juce::String::fromUTF8 (" → ") << facts.candidate;
        g.setColour (facts.updateAvailable() ? skin::accent : skin::textMuted);
        g.drawText (version, line, juce::Justification::centredRight, true);
    }
}

// -- CanvasView -------------------------------------------------------------------

CanvasView::CanvasView (std::vector<Tile> tiles)
{
    setLookAndFeel (&look);
    setOpaque (true);
    confirm = showConfirmation;

    addAndMakeVisible (startAll);
    addAndMakeVisible (stopAll);
    startAll.onClick = [this] {
        if (onStartAll)
            onStartAll();
    };
    stopAll.onClick = [this] {
        askThen ("Stop the whole rig?", "Every deck, the mixer, Motion and Core stop. The sound stops.", [this] {
            if (onStopAll)
                onStopAll();
        });
    };

    for (auto& tile : tiles)
    {
        auto component = std::make_unique<TileComponent> (std::move (tile));
        component->onStart = [this] (const Tile& t) {
            if (onStartTile)
                onStartTile (t);
        };
        // A running program stopped or restarted mid-set cuts the sound: asked once.
        component->onStop = [this] (const Tile& t) {
            askThen ("Stop " + t.label + "?", "It stops now; what it plays stops with it.", [this, t] {
                if (onStopTile)
                    onStopTile (t);
            });
        };
        component->onRestart = [this] (const Tile& t) {
            askThen ("Restart " + t.label + "?", "It stops and starts again; what it plays stops with it.", [this, t] {
                if (onRestartTile)
                    onRestartTile (t);
            });
        };
        addAndMakeVisible (*component);
        tileComponents.push_back (std::move (component));
    }

    log.setMultiLine (true);
    log.setReadOnly (true);
    log.setCaretVisible (false);
    log.setScrollbarsShown (true);
    addAndMakeVisible (log);
    addAndMakeVisible (install);
}

CanvasView::~CanvasView()
{
    setLookAndFeel (nullptr);
}

void CanvasView::askThen (const juce::String& question, const juce::String& detail, std::function<void()> then)
{
    if (confirm)
        confirm (question, detail, std::move (then));
}

void CanvasView::show (const Snapshot& snapshot)
{
    for (size_t i = 0; i < tileComponents.size() && i < snapshot.statuses.size(); ++i)
    {
        const auto& package = tileComponents[i]->getTile().package;
        const auto found = snapshot.facts.packages.find (package);
        tileComponents[i]->setStatus (snapshot.statuses[i], found != snapshot.facts.packages.end() ? found->second.installed : juce::String());
    }
    install.setPackages (snapshot.facts.packages);
}

void CanvasView::appendLog (const juce::String& line)
{
    log.moveCaretToEnd();
    log.insertTextAtCaret ((log.isEmpty() ? juce::String() : juce::String ("\n")) + line);
    const auto lines = juce::StringArray::fromLines (log.getText());
    if (lines.size() > maxLogLines)
    {
        log.setText (juce::StringArray (lines.begin() + (lines.size() - maxLogLines), maxLogLines).joinIntoString ("\n"), false);
        log.moveCaretToEnd();
    }
}

void CanvasView::setBusy (bool busy)
{
    startAll.setEnabled (! busy);
    stopAll.setEnabled (! busy);
    for (auto& tile : tileComponents)
        tile->setBusy (busy);
}

void CanvasView::setSubtitle (const juce::String& text)
{
    subtitle = text;
    repaint (headerArea());
}

juce::Rectangle<int> CanvasView::headerArea() const
{
    const auto m = look.getMetrics();
    auto area = getLocalBounds().reduced (juce::roundToInt (m.padding() * 1.5f));
    return area.removeFromTop (juce::roundToInt (std::max (m.key(), getHeight() * headerShare)));
}

void CanvasView::paint (juce::Graphics& g)
{
    const auto m = look.getMetrics();
    g.fillAll (skin::surface);

    auto header = headerArea();
    const auto text = header.removeFromLeft (header.getWidth() / 2);
    const auto titleHeight = juce::roundToInt (m.title() * 1.3f);
    auto titleArea = text.withHeight (titleHeight).withY (text.getCentreY() - titleHeight / 2 - juce::roundToInt (m.caption() * 0.7f));
    g.setColour (skin::textPrimary);
    g.setFont (font (m.title(), true));
    g.drawText (juce::String::fromUTF8 ("A³ Canvas"), titleArea, juce::Justification::centredLeft, false);
    g.setColour (skin::textMuted);
    g.setFont (font (m.caption()));
    g.drawText (subtitle, titleArea.translated (0, titleHeight).withHeight (juce::roundToInt (m.caption() * 1.6f)),
                juce::Justification::centredLeft, true);

    look.drawCard (g, logCard.toFloat());
    drawCaption (g, "Log", logCard.reduced (juce::roundToInt (m.padding())).withHeight (juce::roundToInt (m.caption() * 1.8f)), m);
}

void CanvasView::resized()
{
    const auto m = Metrics::forWidth (getWidth());
    look.setMetrics (m);
    const int pad = juce::roundToInt (m.padding());
    const int gap = juce::roundToInt (m.gap());

    auto area = getLocalBounds().reduced (juce::roundToInt (m.padding() * 1.5f));
    auto header = area.removeFromTop (headerArea().getHeight());
    const int keyHeight = juce::roundToInt (m.key());
    const int keyWidth = juce::roundToInt (m.key() * 2.4f);
    auto keys = header.withSizeKeepingCentre (header.getWidth(), keyHeight);
    stopAll.setBounds (keys.removeFromRight (keyWidth));
    keys.removeFromRight (gap);
    startAll.setBounds (keys.removeFromRight (keyWidth));
    area.removeFromTop (pad);

    auto bottom = area.removeFromBottom (juce::roundToInt (getHeight() * bottomShare));
    area.removeFromBottom (pad);
    auto packages = bottom.removeFromRight (juce::roundToInt (bottom.getWidth() * 0.4f));
    bottom.removeFromRight (pad);
    install.setBounds (packages);
    logCard = bottom;
    log.setBounds (bottom.reduced (pad).withTrimmedTop (juce::roundToInt (m.caption() * 1.8f)));
    log.applyFontToAllText (juce::Font (juce::FontOptions (juce::Font::getDefaultMonospacedFontName(), m.caption(), juce::Font::plain)));

    // The tiles: two columns on the rig's portrait screen, four on a laptop's landscape one.
    const int columns = landscape (getLocalBounds()) ? 4 : 2;
    const int rows = juce::jmax (1, (static_cast<int> (tileComponents.size()) + columns - 1) / columns);
    juce::Grid grid;
    grid.columnGap = grid.rowGap = juce::Grid::Px (gap);
    for (int c = 0; c < columns; ++c)
        grid.templateColumns.add (juce::Grid::TrackInfo (juce::Grid::Fr (1)));
    for (int r = 0; r < rows; ++r)
        grid.templateRows.add (juce::Grid::TrackInfo (juce::Grid::Fr (1)));
    for (auto& tile : tileComponents)
        grid.items.add (juce::GridItem (*tile));
    grid.performLayout (area);
}
}
