// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CanvasView.h"

namespace canvas
{
namespace
{
// The log takes at least this share of the rig's column, and what tiles past roomyTileShare would leave empty.
constexpr float logShare = 0.25f;
constexpr float roomyTileShare = 1.3f;
// The greeter's share of a landscape page's width.
constexpr float columnShare = 0.3f;
constexpr int maxLogLines = 400;

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

// -- CanvasView -------------------------------------------------------------------

CanvasView::CanvasView (std::vector<Tile> tiles, const juce::String& support) : greeting (support)
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
    addAndMakeVisible (greeting);
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
    greeting.setPackages (snapshot.facts.packages);
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
    repaint (subtitleBox);
}

void CanvasView::paint (juce::Graphics& g)
{
    const auto m = look.getMetrics();
    g.fillAll (skin::surface);

    drawCaption (g, "Rig", rigCaptionBox, m);
    g.setColour (skin::textPrimary);
    g.setFont (canvasFont (m.body()));
    g.drawText (subtitle, subtitleBox, juce::Justification::centredLeft, true);

    look.drawCard (g, logCard.toFloat());
    drawCaption (g, "Log", logCard.reduced (juce::roundToInt (m.padding())).withHeight (juce::roundToInt (m.caption() * 1.8f)), m);
}

void CanvasView::resized()
{
    const auto m = Metrics::forSize (getWidth(), getHeight());
    look.setMetrics (m);
    const int pad = juce::roundToInt (m.padding());

    auto area = getLocalBounds().reduced (juce::roundToInt (m.padding() * 1.5f));
    // Two columns of tiles (or more, see layoutRig) under the band on the rig's portrait screen, four beside the column on a laptop.
    if (landscape (getLocalBounds()))
    {
        greeting.setBounds (area.removeFromLeft (juce::roundToInt (area.getWidth() * columnShare)));
        area.removeFromLeft (juce::roundToInt (m.padding() * 1.5f));
        layoutRig (area, 4);
        return;
    }
    greeting.setBounds (area.removeFromTop (GreeterComponent::bandHeight (m)));
    area.removeFromTop (pad);
    layoutRig (area, 2);
}

// The rig's line with its keys, the tiles, and the log under them.
void CanvasView::layoutRig (juce::Rectangle<int> area, int columns)
{
    const auto m = look.getMetrics();
    const int pad = juce::roundToInt (m.padding());
    const int gap = juce::roundToInt (m.gap());
    const int keyHeight = juce::roundToInt (m.key());
    const int keyWidth = juce::roundToInt (m.key() * 2.4f);

    auto line = area.removeFromTop (keyHeight);
    stopAll.setBounds (line.removeFromRight (keyWidth));
    line.removeFromRight (gap);
    startAll.setBounds (line.removeFromRight (keyWidth));
    line.removeFromRight (pad);
    const int captionHeight = juce::roundToInt (m.caption() * 1.8f);
    auto text = line.withSizeKeepingCentre (line.getWidth(), captionHeight + juce::roundToInt (m.body() * 1.5f));
    rigCaptionBox = text.removeFromTop (captionHeight);
    subtitleBox = text;
    area.removeFromTop (pad);

    // Each tile keeps the height its lines and keys need, and the log a few lines: where the
    // columns asked for leave too few rows of that height, a column more (four decks on the rig).
    const int count = static_cast<int> (tileComponents.size());
    const int leastLog = pad * 2 + captionHeight + juce::roundToInt (m.caption() * 4.0f);
    const auto rowsFor = [count] (int c) { return juce::jmax (1, (count + c - 1) / c); };
    const auto leastTilesFor = [&] (int c) {
        return juce::roundToInt (rowsFor (c) * TileComponent::leastHeight (m)) + (rowsFor (c) - 1) * gap;
    };
    while (columns < count && leastTilesFor (columns) + pad + leastLog > area.getHeight())
        ++columns;
    const int rows = rowsFor (columns);
    const int leastTiles = leastTilesFor (columns);
    // Tiles taller than a third more than they need are only empty card; the log takes the rest.
    const int roomyTiles = juce::roundToInt (rows * TileComponent::leastHeight (m) * roomyTileShare) + (rows - 1) * gap;
    const int logHeight = juce::jmin (area.getHeight() - pad - leastTiles,
                                      juce::jmax (juce::roundToInt (area.getHeight() * logShare), area.getHeight() - pad - roomyTiles));
    logCard = area.removeFromBottom (logHeight);
    area.removeFromBottom (pad);
    log.setBounds (logCard.reduced (pad).withTrimmedTop (captionHeight));
    log.applyFontToAllText (juce::Font (juce::FontOptions (juce::Font::getDefaultMonospacedFontName(), m.caption(), juce::Font::plain)));

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
