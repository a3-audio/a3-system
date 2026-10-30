// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CanvasWindow.h"

#include "model/Demo.h"
#include "sys/Interfaces.h"
#include "sys/SystemRepo.h"

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

// The truth the Canvas names hosts from: the laptop's when written, else the shipped one.
TruthNetwork machineTruth()
{
    const auto laptop = home().getChildFile (".config/a3/laptop/a3-osc.json");
    const auto file = laptop.existsAsFile() ? laptop : shippedTruth;
    return parseTruthNetwork (juce::JSON::parse (file.loadFileAsString()));
}

// Plan R8: the laptop's one truth, when the installer's role laptop has written it.
juce::String laptopTruth()
{
    const auto file = home().getChildFile (".config/a3/laptop/a3-osc.json");
    return file.existsAsFile() ? file.getFullPathName() : juce::String();
}

// Hands commands on until told to stop; after that each one is refused without running.
class StoppableRunner : public CommandRunner
{
public:
    StoppableRunner (CommandRunner& inner, const std::atomic<bool>& stop) : runner (inner), stopping (stop) {}

    int run (const juce::StringArray& argv, const LineCallback& line) override
    {
        return stopping ? -1 : runner.run (argv, line);
    }

private:
    CommandRunner& runner;
    const std::atomic<bool>& stopping;
};

// Git through a runner of its own: the demo's runs nothing, and reading the checkout changes nothing.
std::function<std::pair<SystemFacts, juce::String>()> systemReader (bool withFlashedFirmware)
{
    auto runner = std::make_shared<ProcessRunner>();
    return [runner, withFlashedFirmware] {
        return std::make_pair (readSystem (*runner, machineRepo()),
                               withFlashedFirmware ? machineFlashedMotionFirmware() : juce::String());
    };
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
    setup.support = machineSupport();
    setup.truth = machineTruth();
    setup.systemFacts = systemReader (true);
    return setup;
}

CanvasSetup demoSetup (int decks)
{
    CanvasSetup setup;
    setup.tiles = catalog (decks);
    setup.runner = std::make_unique<DemoRunner>();
    setup.unitFacts = [] (const juce::String&) { return UnitFacts { "loaded", "active", "running", "success", 0 }; };
    setup.demo = true;
    // Support A³ is the project's, not the rig's: the demo shows this machine's.
    setup.support = machineSupport();
    // The demo's addresses are the shipped truth's (192.168.8.x), never made up.
    setup.truth = parseTruthNetwork (juce::JSON::parse (shippedTruth.loadFileAsString()));
    // The system card is this machine's checkout, as it is: a made-up tag would be no status.
    setup.systemFacts = systemReader (false);
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
        auto snapshot = demoSnapshot (tiles, setup.truth);
        if (setup.systemFacts)
            snapshot.facts.system = setup.systemFacts().first;
        view.show (snapshot);
        return;
    }
    view.setSubtitle (juce::SystemStats::getComputerName() + juce::String::fromUTF8 (" · ") + juce::String (tiles.size()) + " programs");
    poller = std::make_unique<StatusPoller> (tiles, *setup.runner, setup.http);
    poller->onSnapshot = [this] (const Snapshot& snapshot) { view.show (snapshot); };
    poller->networkFacts = [truth = setup.truth] { return NetworkFacts { truth, ownAddresses (listInterfaces(), truth) }; };
    poller->systemFacts = setup.systemFacts;
    poller->start();
}

CanvasController::~CanvasController()
{
    *alive = false;
    stopping = true;
    if (poller != nullptr)
        poller->stop();
    // The running command is let finish (a systemctl call returns within its own timeout).
    worker.removeAllJobs (true, -1);
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
        });
    };
    worker.addJob ([this, title, commands = std::move (commands), post] {
        StoppableRunner runner (*setup.runner, stopping);
        const Waiting waiting { 30, [this] {
                                   if (! stopping)
                                       juce::Thread::sleep (500);
                               } };
        const auto result = execute (
            commands, runner, setup.unitFacts, waiting,
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
    auto content = std::make_unique<CanvasView> (setup.tiles, setup.support);
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
