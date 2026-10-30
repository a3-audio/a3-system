// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "sys/StatusPoller.h"
#include "ui/GreeterComponent.h"
#include "ui/LookAndFeel_Canvas.h"
#include "ui/TileComponent.h"

namespace canvas
{
// The Canvas's one page, a welcome first and a control panel second: the greeter, then the rig's
// line with Start all / Stop all, a tile per program, and the log. On the rig's portrait screen the
// greeter is a band across the top; on a landscape screen a column at the left.
class CanvasView : public juce::Component
{
public:
    explicit CanvasView (std::vector<Tile> tiles, const juce::String& support = supportTarget);
    ~CanvasView() override;

    void show (const Snapshot& snapshot);
    void appendLog (const juce::String& line);
    // While a start or stop runs, nothing else may be started (one plan at a time).
    void setBusy (bool busy);
    void setSubtitle (const juce::String& text);

    std::function<void()> onStartAll, onStopAll;
    std::function<void (const Tile&)> onStartTile, onStopTile, onRestartTile;
    // Asks before something that cannot be undone in front of an audience; `then` runs on yes.
    std::function<void (const juce::String& question, const juce::String& detail, std::function<void()> then)> confirm;

    std::vector<std::unique_ptr<TileComponent>>& getTiles() { return tileComponents; }
    juce::TextButton& startAllButton() { return startAll; }
    juce::TextButton& stopAllButton() { return stopAll; }
    juce::TextEditor& logPane() { return log; }
    GreeterComponent& greeter() { return greeting; }
    const juce::String& getSubtitle() const { return subtitle; }
    // Where the rig's line (demo or this machine) is written.
    juce::Rectangle<int> subtitleArea() const { return subtitleBox; }

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    void askThen (const juce::String& question, const juce::String& detail, std::function<void()> then);
    void layoutRig (juce::Rectangle<int> area, int columns);

    LookAndFeel_Canvas look;
    juce::String subtitle;
    juce::Rectangle<int> logCard, rigCaptionBox, subtitleBox;
    juce::TextButton startAll { "Start all" }, stopAll { "Stop all" };
    std::vector<std::unique_ptr<TileComponent>> tileComponents;
    juce::TextEditor log;
    GreeterComponent greeting;
};

void showConfirmation (const juce::String& question, const juce::String& detail, std::function<void()> then);
}
