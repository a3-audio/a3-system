// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <atomic>

#include <juce_gui_basics/juce_gui_basics.h>

#include "model/StartPlan.h"
#include "sys/StatusPoller.h"
#include "ui/CanvasView.h"

namespace canvas
{
// What the window works on: the tiles, the runner every command goes through, where Core answers,
// and the truth the desk is given. The app passes the machine's; --demo and tests pass fakes.
struct CanvasSetup
{
    std::vector<Tile> tiles;
    std::unique_ptr<CommandRunner> runner;
    HttpGet http;
    UnitLookup unitFacts;   // what a start waits on: systemd now (the app), always active (--demo)
    juce::String truthPath;
    SupportConfig support;   // where Support A³ leads, from ~/.config/a3/canvas.json
    TruthNetwork truth;      // the hosts and networks the truth names
    // The umbrella's pins and the flashed Motion firmware (git and install.state; reads only).
    std::function<std::pair<SystemFacts, juce::String>()> systemFacts;
    bool demo = false;
};

// Wires the view to the poller and to the start plans; one plan runs at a time, off the message thread.
class CanvasController
{
public:
    CanvasController (CanvasView& view, CanvasSetup setup);
    ~CanvasController();

    // Runs a plan on the worker thread; refused (false) while another runs.
    bool runPlan (const juce::String& title, std::vector<Command> commands);
    bool isBusy() const { return busy; }

private:
    void finish (const juce::String& title, const PlanResult& result);

    CanvasView& view;
    CanvasSetup setup;
    std::unique_ptr<StatusPoller> poller;
    juce::ThreadPool worker { juce::ThreadPoolOptions{}.withNumberOfThreads (1) };
    bool busy = false;
    std::shared_ptr<bool> alive = std::make_shared<bool> (true);
    // Set when the window goes: the running plan runs no further command and waits no longer.
    std::atomic<bool> stopping { false };
};

class CanvasWindow : public juce::DocumentWindow
{
public:
    explicit CanvasWindow (CanvasSetup setup);
    ~CanvasWindow() override;
    void closeButtonPressed() override;

private:
    CanvasView* view = nullptr;
    std::unique_ptr<CanvasController> controller;
};

// The setup for this machine: deck count from install.conf and the truth, the real runner and HTTP.
CanvasSetup machineSetup();
CanvasSetup demoSetup (int decks);
}
