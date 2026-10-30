// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <set>

#include <gtest/gtest.h>
#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Demo.h"
#include "model/Greeter.h"
#include "ui/CanvasWindow.h"

using namespace canvas;

namespace
{
// The rig's screen.
constexpr int rigWidth = 768, rigHeight = 1024;

TileStatus statusWith (Light light)
{
    TileStatus status;
    status.light = light;
    status.line = "a line";
    return status;
}

juce::Image paintedTile (TileComponent& tile, LookAndFeel_Canvas& look)
{
    look.setMetrics (Metrics::forWidth (rigWidth));
    tile.setLookAndFeel (&look);
    tile.setSize (rigWidth / 2, 200);
    return tile.createComponentSnapshot (tile.getLocalBounds(), true, 1.0f);
}

bool near (juce::Colour a, juce::Colour b, int tolerance = 6)
{
    return std::abs (a.getRed() - b.getRed()) <= tolerance && std::abs (a.getGreen() - b.getGreen()) <= tolerance
           && std::abs (a.getBlue() - b.getBlue()) <= tolerance;
}

int pixelsUnlike (const juce::Image& image, juce::Rectangle<int> area, juce::Colour ground)
{
    int count = 0;
    for (int y = area.getY(); y < area.getBottom(); ++y)
        for (int x = area.getX(); x < area.getRight(); ++x)
            count += near (image.getPixelAt (x, y), ground, 12) ? 0 : 1;
    return count;
}

double lumaVariance (const juce::Image& image)
{
    double sum = 0, squares = 0;
    const int n = image.getWidth() * image.getHeight();
    for (int y = 0; y < image.getHeight(); ++y)
        for (int x = 0; x < image.getWidth(); ++x)
        {
            const double luma = image.getPixelAt (x, y).getPerceivedBrightness() * 255.0;
            sum += luma;
            squares += luma * luma;
        }
    const double mean = sum / n;
    return squares / n - mean * mean;
}

Tile deckTile() { return catalog (1)[1]; }

juce::Colour over (juce::Colour top, juce::Colour ground) { return ground.overlaidWith (top); }

void pumpUntil (const std::function<bool()>& done)
{
    for (int i = 0; i < 200 && ! done(); ++i)
        juce::MessageManager::getInstance()->runDispatchLoopUntil (10);
}
}

// A paint test per light (memory "A page test must paint"): the light's colour at its centre, the label drawn.
TEST (TileComponent, EachLightPaintsItsColour)
{
    for (const auto light : { Light::running, Light::degraded, Light::failed })
    {
        LookAndFeel_Canvas look;
        TileComponent tile (deckTile());
        tile.setStatus (statusWith (light), "03.0");
        const auto image = paintedTile (tile, look);
        const auto centre = tile.lightArea().getCentre().toInt();
        EXPECT_TRUE (near (image.getPixelAt (centre.x, centre.y), lightColour (light)))
            << static_cast<int> (light) << ": " << image.getPixelAt (centre.x, centre.y).toDisplayString (false);
        EXPECT_GT (pixelsUnlike (image, tile.labelArea(), skin::surfaceRaised), 50) << "the label is drawn";
        tile.setLookAndFeel (nullptr);
    }
}

TEST (TileComponent, StartingIsTheAccentDimmed)
{
    LookAndFeel_Canvas look;
    TileComponent tile (deckTile());
    tile.setStatus (statusWith (Light::starting), {});
    const auto image = paintedTile (tile, look);
    const auto centre = tile.lightArea().getCentre().toInt();
    const auto expected = over (skin::accent.withAlpha (skin::alphaMuted), over (skin::accent.withAlpha (skin::alphaOutline), skin::surfaceRaised));
    EXPECT_TRUE (near (image.getPixelAt (centre.x, centre.y), expected)) << image.getPixelAt (centre.x, centre.y).toDisplayString (false);
    tile.setLookAndFeel (nullptr);
}

TEST (TileComponent, StoppedIsAMutedDotAndMissingAnEmptyRing)
{
    LookAndFeel_Canvas look;
    TileComponent stopped (deckTile());
    stopped.setStatus (statusWith (Light::stopped), {});
    auto image = paintedTile (stopped, look);
    auto centre = stopped.lightArea().getCentre().toInt();
    EXPECT_TRUE (near (image.getPixelAt (centre.x, centre.y), over (skin::textMuted.withAlpha (skin::alphaMuted), skin::surfaceRaised)));
    stopped.setLookAndFeel (nullptr);

    TileComponent missing (deckTile());
    missing.setStatus (statusWith (Light::missing), {});
    image = paintedTile (missing, look);
    centre = missing.lightArea().getCentre().toInt();
    EXPECT_TRUE (near (image.getPixelAt (centre.x, centre.y), skin::surfaceRaised)) << "a ring, empty inside";
    EXPECT_GT (pixelsUnlike (image, missing.lightArea().toNearestInt(), skin::surfaceRaised), 10) << "the ring is drawn";
    missing.setLookAndFeel (nullptr);
}

TEST (TileComponent, TheKeyFollowsTheState)
{
    TileComponent tile (deckTile());
    tile.setStatus (statusWith (Light::running), {});
    EXPECT_EQ (tile.startStopButton().getButtonText(), "Stop");
    tile.setStatus (statusWith (Light::stopped), {});
    EXPECT_EQ (tile.startStopButton().getButtonText(), "Start");
    EXPECT_FALSE (tile.restartButton().isEnabled()) << "nothing to restart";
    tile.setStatus (statusWith (Light::missing), {});
    EXPECT_FALSE (tile.startStopButton().isEnabled()) << "nothing to start without the package";
}

TEST (CanvasView, EightTilesForFourDecks)
{
    CanvasView view (catalog (4));
    view.setSize (rigWidth, rigHeight);
    ASSERT_EQ (view.getTiles().size(), 8u);
    for (size_t i = 0; i < view.getTiles().size(); ++i)
    {
        const auto bounds = view.getTiles()[i]->getBounds();
        EXPECT_TRUE (view.getLocalBounds().contains (bounds)) << i;
        EXPECT_GE (bounds.getHeight(), Metrics::forWidth (rigWidth).key() * 2) << i;
        for (size_t j = i + 1; j < view.getTiles().size(); ++j)
            EXPECT_FALSE (bounds.intersects (view.getTiles()[j]->getBounds())) << i << " and " << j;
        EXPECT_GE (view.getTiles()[i]->startStopButton().getHeight(), juce::roundToInt (Metrics::forWidth (rigWidth).key()) - 1)
            << "a key mid-set is a fingertip and more";
    }
}

TEST (CanvasView, StopAllAsksFirst)
{
    CanvasView view (catalog (2));
    int stops = 0;
    std::function<void()> answerYes;
    view.onStopAll = [&] { ++stops; };
    view.confirm = [&] (const juce::String&, const juce::String&, std::function<void()> then) { answerYes = then; };
    view.stopAllButton().triggerClick();
    pumpUntil ([&] { return answerYes != nullptr; });
    ASSERT_TRUE (answerYes != nullptr) << "a question was asked";
    EXPECT_EQ (stops, 0) << "nothing stops before the answer";
    answerYes();
    EXPECT_EQ (stops, 1);
}

TEST (CanvasView, StoppingARunningTileAsksFirstStartingDoesNot)
{
    CanvasView view (catalog (1));
    auto& deck = *view.getTiles()[1];
    int asked = 0, started = 0, stopped = 0;
    view.confirm = [&] (const juce::String&, const juce::String&, std::function<void()> then) { ++asked; then(); };
    view.onStartTile = [&] (const Tile&) { ++started; };
    view.onStopTile = [&] (const Tile&) { ++stopped; };

    deck.setStatus (statusWith (Light::stopped), {});
    deck.startStopButton().triggerClick();
    pumpUntil ([&] { return started > 0; });
    EXPECT_EQ (started, 1);
    EXPECT_EQ (asked, 0);

    deck.setStatus (statusWith (Light::running), {});
    deck.startStopButton().triggerClick();
    pumpUntil ([&] { return stopped > 0; });
    EXPECT_EQ (asked, 1);
    EXPECT_EQ (stopped, 1);
}

TEST (CanvasWindow, ButtonsAreOffWhileAPlanRuns)
{
    CanvasView view (catalog (2));
    CanvasController controller (view, demoSetup (2));
    EXPECT_TRUE (controller.runPlan ("Start all", startAll (catalog (2), {})));
    EXPECT_FALSE (view.startAllButton().isEnabled());
    EXPECT_FALSE (view.getTiles()[0]->startStopButton().isEnabled());
    EXPECT_FALSE (controller.runPlan ("again", startAll (catalog (2), {}))) << "one plan at a time";
    pumpUntil ([&] { return ! controller.isBusy(); });
    EXPECT_TRUE (view.startAllButton().isEnabled());
    EXPECT_TRUE (view.logPane().getText().contains ("demo, not run: systemctl --user start a3-engine.service"));
    EXPECT_TRUE (view.logPane().getText().contains ("Start all: done"));
}

// The demo is the rig as the maintainer described it: everything up but the last deck.
TEST (CanvasWindow, TheDemoShowsARunningRigWithTheLastDeckStopped)
{
    CanvasView view (catalog (4));
    CanvasController controller (view, demoSetup (4));
    for (const auto& tile : view.getTiles())
    {
        const auto expected = tile->getTile().id == "deck-D" ? Light::stopped : Light::running;
        EXPECT_EQ (tile->getStatus().light, expected) << tile->getTile().id;
    }
    view.setSize (rigWidth, rigHeight);
    const auto image = view.createComponentSnapshot (view.getLocalBounds(), true, 1.0f);
    EXPECT_GT (lumaVariance (image), 50.0) << "the page paints";
}

// -- The greeter -------------------------------------------------------------------

namespace
{
constexpr int laptopWidth = 1920, laptopHeight = 1080;
const juce::Colour logoInk { 255, 255, 243 };   // the website's logo fill, #FFFFF3

int pixelsNear (const juce::Image& image, juce::Rectangle<int> area, juce::Colour colour, int tolerance = 12)
{
    int count = 0;
    area = area.getIntersection (image.getBounds());
    for (int y = area.getY(); y < area.getBottom(); ++y)
        for (int x = area.getX(); x < area.getRight(); ++x)
            count += near (image.getPixelAt (x, y), colour, tolerance) ? 1 : 0;
    return count;
}

juce::Image snapshotOf (juce::Component& component) { return component.createComponentSnapshot (component.getLocalBounds(), true, 1.0f); }

std::map<juce::String, PackageFacts> allInstalled()
{
    std::map<juce::String, PackageFacts> packages;
    for (const auto& name : greeterPackages())
        packages[name] = { "03.0+800", "03.0+800" };
    return packages;
}

// A greeter on its own, in the Canvas's look, as the band of the rig's screen.
struct LookedGreeter
{
    LookAndFeel_Canvas look;
    GreeterComponent greeter;

    explicit LookedGreeter (const juce::String& support = {}) : greeter (support, "0.1.0")
    {
        greeter.setLookAndFeel (&look);
        greeter.setSize (rigWidth, GreeterComponent::bandHeight (look.getMetrics()));
    }
    ~LookedGreeter() { greeter.setLookAndFeel (nullptr); }
};

// Where a component sits in the view, in the view's coordinates.
juce::Rectangle<int> inView (CanvasView& view, juce::Component& child) { return view.getLocalArea (&child, child.getLocalBounds()); }

void expectTheWholePageFits (CanvasView& view)
{
    const auto greeter = view.greeter().getBounds();
    const auto key = Metrics::forSize (view.getWidth(), view.getHeight()).key();
    EXPECT_TRUE (view.getLocalBounds().contains (greeter));
    for (auto* button : { &view.startAllButton(), &view.stopAllButton() })
    {
        EXPECT_FALSE (button->getBounds().intersects (greeter)) << "the rig's keys are not the greeter's";
        EXPECT_GE (button->getHeight(), juce::roundToInt (key) - 1) << "a fingertip and more";
    }
    for (size_t i = 0; i < view.getTiles().size(); ++i)
    {
        const auto tile = view.getTiles()[i]->getBounds();
        EXPECT_TRUE (view.getLocalBounds().contains (tile)) << i;
        EXPECT_FALSE (tile.intersects (greeter)) << i;
        EXPECT_GE (tile.getHeight(), TileComponent::leastHeight (Metrics::forSize (view.getWidth(), view.getHeight())) - 1)
            << i << ": its lines clear its keys";
    }
    EXPECT_GE (view.logPane().getHeight(), Metrics::forSize (view.getWidth(), view.getHeight()).caption() * 3) << "the log has lines";
}
}

// The rig's portrait screen: the greeter across the top, the rig under it.
TEST (CanvasView, TheGreeterLeadsThePageOnTheRigsScreen)
{
    CanvasView view (catalog (4));
    view.setSize (rigWidth, rigHeight);
    expectTheWholePageFits (view);
    for (const auto& tile : view.getTiles())
        EXPECT_GE (tile->getY(), view.greeter().getBottom());
    EXPECT_GE (view.startAllButton().getY(), view.greeter().getBottom());
    EXPECT_LT (view.greeter().getY(), view.getHeight() / 10) << "it is the first thing on the page";
}

// Fewer decks, fewer tiles: two columns again when they fit.
TEST (CanvasView, TwoDecksKeepTwoColumnsOnTheRigsScreen)
{
    CanvasView view (catalog (2));
    view.setSize (rigWidth, rigHeight);
    expectTheWholePageFits (view);
    std::set<int> columns;
    for (const auto& tile : view.getTiles())
        columns.insert (tile->getX());
    EXPECT_EQ (columns.size(), 2u);
}

// A laptop's landscape screen: the greeter as a column at the left, the rig beside it.
TEST (CanvasView, TheGreeterIsAColumnBesideTheRigOnALaptop)
{
    CanvasView view (catalog (4));
    view.setSize (laptopWidth, laptopHeight);
    expectTheWholePageFits (view);
    for (const auto& tile : view.getTiles())
        EXPECT_GE (tile->getX(), view.greeter().getRight());
    EXPECT_GT (view.greeter().getHeight(), laptopHeight / 2);
}

TEST (Greeter, TheLinksAreHyperlinksToTheirTargets)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    ASSERT_EQ (greeter.getLinks().size(), 3);
    const auto expected = greeterLinks ({});
    for (int i = 0; i < greeter.getLinks().size(); ++i)
    {
        EXPECT_EQ (greeter.getLinks()[i]->getButtonText(), expected[(size_t) i].label);
        EXPECT_EQ (greeter.getLinks()[i]->getURL().toString (false), expected[(size_t) i].url);
    }
}

TEST (Greeter, NoSupportKeyWhileUnsetOneWhenSet)
{
    const auto labels = [] (GreeterComponent& g) {
        juce::StringArray texts;
        for (auto* link : g.getLinks())
            if (link->isVisible())
                texts.add (link->getButtonText());
        return texts;
    };
    LookedGreeter unset;
    EXPECT_FALSE (labels (unset.greeter).contains (juce::String::fromUTF8 ("Support A³")));

    LookedGreeter looked ("https://example.org/support");
    auto& set = looked.greeter;
    ASSERT_TRUE (labels (set).contains (juce::String::fromUTF8 ("Support A³")));
    auto* support = set.getLinks().getLast();
    EXPECT_TRUE (set.getLocalBounds().contains (support->getBounds()));
    EXPECT_GT (pixelsUnlike (snapshotOf (set), support->getBounds(), skin::surface), 30) << "the key paints";
}

// A paint test per state (memory "A page test must paint").
TEST (Greeter, TheLogoPaintsInTheWebsitesInkAtBothSizes)
{
    for (const auto& size : { juce::Point<int> (rigWidth, rigHeight), juce::Point<int> (laptopWidth, laptopHeight) })
    {
        CanvasView view (catalog (4));
        view.setSize (size.x, size.y);
        const auto image = snapshotOf (view);
        const auto logo = view.getLocalArea (&view.greeter(), view.greeter().logoArea().toNearestInt());
        EXPECT_GT (logo.getHeight(), Metrics::forSize (size.x, size.y).key() * 1.5f) << size.x << ": the logo leads";
        EXPECT_GT (pixelsNear (image, logo, logoInk), logo.getWidth() * logo.getHeight() / 20) << size.x;
        EXPECT_EQ (pixelsNear (image, view.getLocalBounds().withTrimmedTop (view.greeter().getBottom()), logoInk), 0)
            << size.x << ": the logo's ink is the logo's alone";
    }
}

TEST (Greeter, InstalledVersionsPaintInTextAndMissingOnesMuted)
{
    LookedGreeter lookedInstalled;
    auto& installed = lookedInstalled.greeter;
    installed.setPackages (allInstalled());
    auto image = snapshotOf (installed);
    EXPECT_GT (pixelsNear (image, installed.versionsArea(), skin::textPrimary, 20), 40) << "the versions are read";

    LookedGreeter lookedMissing;
    auto& missing = lookedMissing.greeter;
    auto packages = allInstalled();
    for (auto& [name, facts] : packages)
        facts.installed = {};
    missing.setPackages (packages);
    image = snapshotOf (missing);
    const auto canvasRow = missing.versionRowArea (static_cast<int> (greeterPackages().size()));
    for (int row = 0; row < static_cast<int> (greeterPackages().size()); ++row)
        EXPECT_EQ (pixelsNear (image, missing.versionRowArea (row), skin::textPrimary, 20), 0) << row << ": not installed, not lit";
    EXPECT_GT (pixelsNear (image, canvasRow, skin::textPrimary, 20), 10) << "the Canvas itself runs";
    EXPECT_GT (pixelsUnlike (image, missing.versionsArea(), skin::surfaceRaised), 200) << "but it is all written";
}

TEST (Greeter, AnUpdatePaintsInTheAccent)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    auto packages = allInstalled();
    packages["stemdeck"].candidate = "03.0+900";
    greeter.setPackages (packages);
    EXPECT_GT (pixelsNear (snapshotOf (greeter), greeter.versionRowArea (1), skin::accent, 20), 10);
}

TEST (Greeter, TheLicenceLineIsWritten)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    EXPECT_GT (pixelsUnlike (snapshotOf (greeter), greeter.licenceArea(), skin::surfaceRaised), 100);
}

TEST (CanvasWindow, TheDemoSaysItIsADemo)
{
    CanvasView view (catalog (4));
    CanvasController controller (view, demoSetup (4));
    EXPECT_TRUE (view.getSubtitle().startsWith ("Demo"));
    view.setSize (rigWidth, rigHeight);
    const auto image = snapshotOf (view);
    EXPECT_GT (pixelsUnlike (image, view.subtitleArea(), skin::surface), 100) << "and paints it";
    EXPECT_GT (pixelsNear (image, inView (view, view.greeter()), skin::textPrimary, 20), 200) << "the demo's versions";
}

// For the maintainer's eye: with A3CANVAS_SNAPSHOT_DIR set, the demo at the rig's size as a PNG.
TEST (CanvasWindow, WritesTheRigSizedScreenForReview)
{
    const auto directory = juce::SystemStats::getEnvironmentVariable ("A3CANVAS_SNAPSHOT_DIR", {});
    if (directory.isEmpty())
        GTEST_SKIP() << "A3CANVAS_SNAPSHOT_DIR not set";
    CanvasView view (catalog (4));
    CanvasController controller (view, demoSetup (4));
    view.setSize (rigWidth, rigHeight);
    view.appendLog ("-- Start all");
    for (const auto& command : startAll (catalog (4), "/home/dj/.config/a3/laptop/a3-osc.json"))
        view.appendLog ("$ " + command.argv.joinIntoString (" "));
    view.appendLog ("Start all: done");
    const auto file = juce::File (directory).getChildFile ("a3-canvas.png");
    ASSERT_TRUE (file.getParentDirectory().createDirectory().wasOk());
    file.deleteFile();
    juce::FileOutputStream stream (file);
    ASSERT_TRUE (stream.openedOk());
    ASSERT_TRUE (juce::PNGImageFormat().writeImageToStream (view.createComponentSnapshot (view.getLocalBounds(), true, 1.0f), stream));

    view.setSize (1920, 1080);
    const auto laptop = juce::File (directory).getChildFile ("a3-canvas-laptop.png");
    laptop.deleteFile();
    juce::FileOutputStream laptopStream (laptop);
    ASSERT_TRUE (laptopStream.openedOk());
    ASSERT_TRUE (juce::PNGImageFormat().writeImageToStream (view.createComponentSnapshot (view.getLocalBounds(), true, 1.0f), laptopStream));
}

namespace
{
// Every command takes a while; nothing ever becomes active, so each start waits its full time.
class SlowRunner : public CommandRunner
{
public:
    explicit SlowRunner (std::atomic<int>& ranCount) : ran (ranCount) {}
    int run (const juce::StringArray&, const LineCallback&) override
    {
        ++ran;
        juce::Thread::sleep (50);
        return 0;
    }

private:
    std::atomic<int>& ran;
};
}

// Quitting during Start all neither hangs the window for the plan's waits nor starts the rest.
TEST (CanvasWindow, ClosingDuringAPlanStopsIt)
{
    std::atomic<int> ran { 0 };
    CanvasView view (catalog (4));
    auto setup = demoSetup (4);
    setup.runner = std::make_unique<SlowRunner> (ran);
    setup.unitFacts = [] (const juce::String&) { return UnitFacts { "loaded", "activating", "start", "success", 0 }; };
    const auto commands = startAll (setup.tiles, {});
    auto controller = std::make_unique<CanvasController> (view, std::move (setup));
    ASSERT_TRUE (controller->runPlan ("Start all", commands));
    juce::Thread::sleep (200);   // inside the engine's wait

    const auto before = juce::Time::getMillisecondCounter();
    controller = nullptr;
    EXPECT_LT (juce::Time::getMillisecondCounter() - before, 2000u);
    EXPECT_LT (ran.load(), static_cast<int> (commands.size()));
}
