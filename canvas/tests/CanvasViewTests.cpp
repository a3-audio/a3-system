// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>
#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Demo.h"
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
}
