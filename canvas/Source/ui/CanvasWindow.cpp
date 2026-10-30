// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CanvasWindow.h"

#include "model/Demo.h"

namespace canvas
{
namespace
{
const juce::File shippedTruth ("/usr/share/a3/a3-osc.json");
constexpr int defaultDecks = 4;

juce::File home() { return juce::File::getSpecialLocation (juce::File::userHomeDirectory); }

int machineDecks()
{
    const auto truth = juce::JSON::parse (shippedTruth.loadFileAsString());
    const int truthDecks = truthDeckCount (truth, defaultDecks);
    return decksFromInstallConf (home().getChildFile (".config/a3/install.conf").loadFileAsString(), truthDecks);
}

// Plan R8: the laptop's one truth, when the installer's role laptop has written it.
juce::String laptopTruth()
{
    const auto file = home().getChildFile (".config/a3/laptop/a3-osc.json");
    return file.existsAsFile() ? file.getFullPathName() : juce::String();
}

UnitFacts unitFactsNow (CommandRunner& runner, const juce::String& unit)
{
    const auto units = parseSystemctlShow (outputOf (runner, showCommand ({ unit })));
    const auto found = units.find (unit);
    return found != units.end() ? found->second : UnitFacts {};
}
}

CanvasSetup machineSetup()
{
    CanvasSetup setup;
    setup.tiles = catalog (machineDecks());
    setup.runner = std::make_unique<ProcessRunner>();
    setup.http = httpGetLocal;
    setup.unitFacts = [runner = setup.runner.get()] (const juce::String& unit) { return unitFactsNow (*runner, unit); };
    setup.truthPath = laptopTruth();
    return setup;
}

CanvasSetup demoSetup (int decks)
{
    CanvasSetup setup;
    setup.tiles = catalog (decks);
    setup.runner = std::make_unique<DemoRunner>();
    setup.unitFacts = [] (const juce::String&) { return UnitFacts { "loaded", "active", "running", "success", 0 }; };
    setup.demo = true;
    return setup;
}

// -- CanvasController ----------------------------------------------------------

CanvasController::CanvasController (CanvasView& v, CanvasSetup s) : view (v), setup (std::move (s))
{
    const auto& tiles = setup.tiles;
    view.onStartAll = [this, tiles] { runPlan ("Start all", startAll (tiles, setup.truthPath)); };
    view.onStopAll = [this, tiles] { runPlan ("Stop all", stopAll (tiles)); };
    view.onStartTile = [this] (const Tile& t) { runPlan ("Start " + t.label, startTile (t, setup.truthPath)); };
    view.onStopTile = [this] (const Tile& t) { runPlan ("Stop " + t.label, stopTile (t)); };
    view.onRestartTile = [this] (const Tile& t) { runPlan ("Restart " + t.label, restartTile (t, setup.truthPath)); };

    if (setup.demo)
    {
        view.setSubtitle (juce::String::fromUTF8 ("Demo · a made-up rig, connected to nothing"));
        view.show (demoSnapshot (tiles));
        return;
    }
    view.setSubtitle (juce::SystemStats::getComputerName() + juce::String::fromUTF8 (" · ") + juce::String (tiles.size()) + " programs");
    poller = std::make_unique<StatusPoller> (tiles, *setup.runner, setup.http);
    poller->onSnapshot = [this] (const Snapshot& snapshot) { view.show (snapshot); };
    poller->start();
}

CanvasController::~CanvasController()
{
    *alive = false;
    if (poller != nullptr)
        poller->stop();
    worker.removeAllJobs (true, 20000);
}

bool CanvasController::runPlan (const juce::String& title, std::vector<Command> commands)
{
    if (busy)
        return false;
    busy = true;
    view.setBusy (true);
    view.appendLog ("-- " + title);

    auto weakAlive = std::weak_ptr<bool> (alive);
    const auto post = [this, weakAlive] (std::function<void()> onMessageThread) {
        juce::MessageManager::callAsync ([this, weakAlive, onMessageThread] {
            if (auto still = weakAlive.lock(); still && *still)
                onMessageThread();
            juce::ignoreUnused (this);
        });
    };
    worker.addJob ([this, title, commands = std::move (commands), post] {
        const auto result = execute (
            commands, *setup.runner, setup.unitFacts, {},
            [post, this] (const juce::String& line) { post ([this, line] { view.appendLog (line); }); });
        post ([this, title, result] { finish (title, result); });
    });
    return true;
}

void CanvasController::finish (const juce::String& title, const PlanResult& result)
{
    for (const auto& skipped : result.skipped)
        view.appendLog (skipped + ": not started, waiting for the engine");
    view.appendLog (result.ok() ? title + ": done" : title + ": " + juce::String (result.failed.size()) + " failed, "
                                                       + juce::String (result.skipped.size()) + " skipped");
    busy = false;
    view.setBusy (false);
}

// -- CanvasWindow --------------------------------------------------------------------

CanvasWindow::CanvasWindow (CanvasSetup setup)
    : juce::DocumentWindow (juce::String::fromUTF8 ("A³ Canvas"), skin::surface, juce::DocumentWindow::allButtons)
{
    auto content = std::make_unique<CanvasView> (setup.tiles);
    view = content.get();
    controller = std::make_unique<CanvasController> (*view, std::move (setup));
    setUsingNativeTitleBar (true);
    setContentOwned (content.release(), false);
    setResizable (true, true);
    // The rig's screen is 768 × 1024 portrait; on a larger screen the same page, scaled.
    const auto screen = juce::Desktop::getInstance().getDisplays().getPrimaryDisplay();
    const auto area = screen != nullptr ? screen->userBounds : juce::Rectangle<float> (768.0f, 1024.0f);
    const float scale = std::min (1.0f, std::min (area.getWidth() / 768.0f, area.getHeight() / 1024.0f));
    centreWithSize (juce::roundToInt (768 * scale), juce::roundToInt (1024 * scale));
}

CanvasWindow::~CanvasWindow()
{
    controller = nullptr;
    clearContentComponent();
}

void CanvasWindow::closeButtonPressed()
{
    juce::JUCEApplication::getInstance()->systemRequestedQuit();
}
}
