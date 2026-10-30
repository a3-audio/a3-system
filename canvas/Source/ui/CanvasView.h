// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "sys/StatusPoller.h"
#include "ui/LookAndFeel_Canvas.h"
#include "ui/TileComponent.h"

namespace canvas
{
// The packages the rig is made of, installed against what apt offers. Install, Update and Remove
// come with the installer interface (plan Tasks 17 and 22); until then no key that does nothing.
class InstallPanel : public juce::Component
{
public:
    void setPackages (const std::map<juce::String, PackageFacts>& packages);
    void paint (juce::Graphics&) override;

private:
    Metrics metrics() const;
    std::map<juce::String, PackageFacts> packages;
};

// The Canvas's one page: a header with Start all / Stop all, a tile per program, the log, the packages.
class CanvasView : public juce::Component
{
public:
    explicit CanvasView (std::vector<Tile> tiles);
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

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    void askThen (const juce::String& question, const juce::String& detail, std::function<void()> then);
    juce::Rectangle<int> headerArea() const;

    LookAndFeel_Canvas look;
    juce::String subtitle;
    juce::Rectangle<int> logCard;
    juce::TextButton startAll { "Start all" }, stopAll { "Stop all" };
    std::vector<std::unique_ptr<TileComponent>> tileComponents;
    juce::TextEditor log;
    InstallPanel install;
};

void showConfirmation (const juce::String& question, const juce::String& detail, std::function<void()> then);
}
