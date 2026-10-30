// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/TileStatus.h"
#include "ui/LookAndFeel_Canvas.h"

namespace canvas
{
// One program of the rig: its light, its name, what it is doing, and Start/Stop and Restart.
class TileComponent : public juce::Component
{
public:
    explicit TileComponent (Tile tile);

    void setStatus (const TileStatus& status, const juce::String& version);
    void setBusy (bool busy);

    const Tile& getTile() const { return tile; }
    const TileStatus& getStatus() const { return status; }
    juce::TextButton& startStopButton() { return startStop; }
    juce::TextButton& restartButton() { return restart; }

    // The height at which the label, caption and line clear the keys.
    static float leastHeight (const Metrics& m);

    // Where the light and the label are drawn (tests look there).
    juce::Rectangle<float> lightArea() const;
    juce::Rectangle<int> labelArea() const;

    std::function<void (const Tile&)> onStart, onStop, onRestart;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    Metrics metrics() const;
    bool isUp() const;
    void updateButtons();

    Tile tile;
    TileStatus status;
    juce::String version;
    bool busy = false;
    juce::TextButton startStop, restart { "Restart" };
};
}
