// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CanvasView.h"

#include "model/Hosts.h"

namespace canvas
{
namespace
{
// The greeter's share of a landscape page's width.
constexpr float columnShare = 0.3f;
constexpr int maxLogLines = 400;

bool landscape (juce::Rectangle<int> area) { return area.getWidth() > area.getHeight(); }
int captionRow (const Metrics& m) { return juce::roundToInt (m.caption() * 1.8f); }
int rowGap (const Metrics& m) { return juce::roundToInt (m.gap() * 0.5f); }
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

CanvasView::CanvasView (std::vector<Tile> tiles, SupportConfig support) : greeting (std::move (support))
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
        tileComponents[i]->setHost (hostLine (tileComponents[i]->getTile(), snapshot.facts));
    }
    greeting.setMachineLine (machineLine (snapshot.facts.network.own));
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
    drawCaption (g, "Decks", decksCaptionBox, m);
    drawCaption (g, "System", systemCaptionBox, m);

    if (logCard.isEmpty())
        return;
    look.drawCard (g, logCard.toFloat());
    drawCaption (g, "Log", logCard.reduced (juce::roundToInt (m.padding())).withHeight (captionRow (m)), m);
}

void CanvasView::resized()
{
    const auto m = Metrics::forSize (getWidth(), getHeight());
    look.setMetrics (m);
    const int pad = juce::roundToInt (m.padding());

    auto area = getLocalBounds().reduced (juce::roundToInt (m.padding() * 1.5f));
    if (landscape (getLocalBounds()))
    {
        greeting.setBounds (area.removeFromLeft (juce::roundToInt (area.getWidth() * columnShare)));
        area.removeFromLeft (juce::roundToInt (m.padding() * 1.5f));
    }
    else
    {
        greeting.setBounds (area.removeFromTop (GreeterComponent::bandHeight (m, greeting.supportCard().getConfig())));
        area.removeFromTop (pad);
    }
    layoutRig (area);
}

juce::Rectangle<int> CanvasView::layoutSection (juce::Rectangle<int> area, bool decks, juce::Rectangle<int>& caption)
{
    const auto m = look.getMetrics();
    caption = area.removeFromTop (captionRow (m));
    const int rowHeight = juce::roundToInt (TileComponent::rowHeight (m));
    bool first = true;
    for (auto& row : tileComponents)
    {
        if ((row->getTile().kind == TileKind::deck) != decks)
            continue;
        if (! first)
            area.removeFromTop (rowGap (m));
        row->setBounds (area.removeFromTop (rowHeight));
        first = false;
    }
    return area;
}

// The rig's line with its keys, the two sections, and the log in what is left: the log gives way
// first when the page is short, never a row.
void CanvasView::layoutRig (juce::Rectangle<int> area)
{
    const auto m = look.getMetrics();
    const int pad = juce::roundToInt (m.padding());
    const int keyHeight = juce::roundToInt (m.key());
    const int keyWidth = juce::roundToInt (m.key() * 2.4f);

    auto line = area.removeFromTop (keyHeight);
    stopAll.setBounds (line.removeFromRight (keyWidth));
    line.removeFromRight (juce::roundToInt (m.gap()));
    startAll.setBounds (line.removeFromRight (keyWidth));
    line.removeFromRight (pad);
    auto text = line.withSizeKeepingCentre (line.getWidth(), captionRow (m) + juce::roundToInt (m.body() * 1.5f));
    rigCaptionBox = text.removeFromTop (captionRow (m));
    subtitleBox = text;
    area.removeFromTop (pad);

    area = layoutSection (area, true, decksCaptionBox);
    area.removeFromTop (pad);
    area = layoutSection (area, false, systemCaptionBox);
    area.removeFromTop (pad);

    const bool roomForLog = area.getHeight() >= pad * 2 + captionRow (m) + juce::roundToInt (m.caption() * 2.0f);
    logCard = roomForLog ? area : juce::Rectangle<int>();
    log.setVisible (roomForLog);
    log.setBounds (logCard.reduced (pad).withTrimmedTop (captionRow (m)));
    log.applyFontToAllText (juce::Font (juce::FontOptions (juce::Font::getDefaultMonospacedFontName(), m.caption(), juce::Font::plain)));
}
}
