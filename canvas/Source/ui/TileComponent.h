// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/TileStatus.h"
#include "ui/LookAndFeel_Canvas.h"

namespace canvas
{
// One program of the rig as a row of the list: its light, its name, what it is doing, its version,
// and Start/Stop and Restart at the right. (A tile before 2026-10-30; the name stayed.)
class TileComponent : public juce::Component
{
public:
    explicit TileComponent (Tile tile);

    void setStatus (const TileStatus& status, const juce::String& version);
    void setBusy (bool busy);
    // Where it runs ("local · 192.168.8.10", an address, or nothing), muted after its state line.
    void setHost (const juce::String& host);
    const juce::String& getHost() const { return host; }

    const Tile& getTile() const { return tile; }
    const TileStatus& getStatus() const { return status; }
    juce::TextButton& startStopButton() { return startStop; }
    juce::TextButton& restartButton() { return restart; }

    // Every row has this height: its keys and a little air.
    static float rowHeight (const Metrics& m);
    // The keys of a row: smaller than Start all's (a stop asks first), still well above a fingertip.
    static float rowKey (const Metrics& m) { return m.key() * 0.75f; }

    // Where the light, the name and the version are drawn (tests look there).
    juce::Rectangle<float> lightArea() const;
    juce::Rectangle<int> labelArea() const;
    juce::Rectangle<int> versionArea() const;
    juce::Rectangle<int> hostArea() const;

    std::function<void (const Tile&)> onStart, onStop, onRestart;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    bool isUp() const;
    // Name over line, centred in the row, between the light and the version.
    juce::Rectangle<float> textBlock() const;
    void updateButtons();

    Tile tile;
    TileStatus status;
    juce::String version, host;
    bool busy = false;
    juce::TextButton startStop, restart { "Restart" };
};
}
