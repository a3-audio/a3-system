// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <set>

#include <gtest/gtest.h>
#include <juce_gui_basics/juce_gui_basics.h>

#include "model/Demo.h"
#include "model/Greeter.h"
#include "model/Support.h"
#include "Fixtures.h"
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
    tile.setSize (rigWidth, juce::roundToInt (TileComponent::rowHeight (look.getMetrics())));
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

// -- The page ----------------------------------------------------------------------

namespace
{
constexpr int laptopWidth = 1920, laptopHeight = 1080;
const juce::Colour logoInk { 255, 255, 243 };   // the website's logo fill, #FFFFF3
// BIP 173's example address: valid in form, nobody's wallet.
const juce::String exampleAddress = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4";

SupportConfig everySupport() { return { "https://ko-fi.com/example", "https://paypal.me/example", exampleAddress }; }

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

    explicit LookedGreeter (SupportConfig support = {}) : greeter (std::move (support), "0.1.0")
    {
        greeter.setLookAndFeel (&look);
        greeter.setSize (rigWidth, GreeterComponent::bandHeight (look.getMetrics(), greeter.supportCard().getConfig()));
    }
    ~LookedGreeter() { greeter.setLookAndFeel (nullptr); }
};

juce::Rectangle<int> inView (CanvasView& view, juce::Component& child) { return view.getLocalArea (&child, child.getLocalBounds()); }

// Everything on the page by name, in the view's coordinates.
std::vector<std::pair<juce::String, juce::Rectangle<int>>> elementsOf (CanvasView& view)
{
    auto& greeter = view.greeter();
    const auto fromGreeter = [&] (juce::Rectangle<int> r) { return view.getLocalArea (&greeter, r); };
    std::vector<std::pair<juce::String, juce::Rectangle<int>>> elements {
        { "logo", fromGreeter (greeter.logoArea().toNearestInt()) },
        { "tagline", fromGreeter (greeter.taglineArea()) },
        { "about", fromGreeter (greeter.aboutArea()) },
        { "machine line", fromGreeter (greeter.machineLineArea()) },
        { "versions", fromGreeter (greeter.versionsArea()) },
        { "start all", view.startAllButton().getBounds() },
        { "stop all", view.stopAllButton().getBounds() },
        { "rig line", view.subtitleArea() },
        { "decks caption", view.decksCaptionArea() },
        { "system caption", view.systemCaptionArea() },
        { "log", view.logCardArea() },
    };
    for (auto* link : greeter.getLinks())
        elements.push_back ({ "link " + link->getButtonText(), inView (view, *link) });
    if (greeter.supportCard().isVisible())
        elements.push_back ({ "support", inView (view, greeter.supportCard()) });
    for (const auto& row : view.getTiles())
        elements.push_back ({ row->getTile().label, row->getBounds() });
    return elements;
}

void expectEverythingFitsApart (CanvasView& view)
{
    const auto elements = elementsOf (view);
    for (size_t i = 0; i < elements.size(); ++i)
    {
        EXPECT_FALSE (elements[i].second.isEmpty()) << elements[i].first;
        EXPECT_TRUE (view.getLocalBounds().contains (elements[i].second)) << elements[i].first << " is inside the window";
        for (size_t j = i + 1; j < elements.size(); ++j)
            EXPECT_FALSE (elements[i].second.intersects (elements[j].second)) << elements[i].first << " and " << elements[j].first;
    }
    const auto m = Metrics::forSize (view.getWidth(), view.getHeight());
    EXPECT_GE (view.logPane().getHeight(), m.caption() * 3) << "the log keeps a few lines";
    for (const auto& row : view.getTiles())
    {
        EXPECT_GE (row->getHeight(), juce::roundToInt (TileComponent::rowHeight (m)) - 1) << row->getTile().label;
        EXPECT_GE (row->startStopButton().getHeight(), juce::roundToInt (m.key() * 0.7f)) << "a fingertip and more";
    }
}
}

// The design target for now: the whole page on the rig's 768 × 1024, nothing scrolled, nothing on top of anything.
TEST (CanvasView, EverythingFitsTheRigsScreenWithSupportSet)
{
    CanvasView view (catalog (4), everySupport());
    view.setSize (rigWidth, rigHeight);
    expectEverythingFitsApart (view);
    EXPECT_LT (view.greeter().getY(), view.getHeight() / 10) << "the welcome comes first";
    for (const auto& row : view.getTiles())
        EXPECT_GE (row->getY(), view.greeter().getBottom());
}

TEST (CanvasView, EverythingFitsTheRigsScreenWithoutSupport)
{
    CanvasView view (catalog (4));
    view.setSize (rigWidth, rigHeight);
    expectEverythingFitsApart (view);
    EXPECT_FALSE (view.greeter().supportCard().isVisible());
}

TEST (CanvasView, ALaptopKeepsWorking)
{
    CanvasView view (catalog (4), everySupport());
    view.setSize (laptopWidth, laptopHeight);
    expectEverythingFitsApart (view);
    for (const auto& row : view.getTiles())
        EXPECT_GE (row->getX(), view.greeter().getRight());
}

// Decks first, A to D; then the system: Engine, Mixer, Motion, Beat analyzer. Rows of one height.
TEST (CanvasView, ARowListInTwoSections)
{
    CanvasView view (catalog (4));
    view.setSize (rigWidth, rigHeight);
    std::vector<TileComponent*> rows;
    for (auto& row : view.getTiles())
        rows.push_back (row.get());
    std::sort (rows.begin(), rows.end(), [] (auto* a, auto* b) { return a->getY() < b->getY(); });
    juce::StringArray order;
    for (auto* row : rows)
        order.add (row->getTile().id);
    EXPECT_EQ (order.joinIntoString (" "), "deck-A deck-B deck-C deck-D core mixer motion analyzer");
    for (auto* row : rows)
    {
        EXPECT_EQ (row->getHeight(), rows.front()->getHeight()) << row->getTile().id;
        EXPECT_EQ (row->getX(), rows.front()->getX()) << "one column";
    }
    EXPECT_LT (view.decksCaptionArea().getBottom(), rows[0]->getY() + 1);
    EXPECT_GT (view.systemCaptionArea().getY(), rows[3]->getBottom() - 1);
    EXPECT_LT (view.systemCaptionArea().getBottom(), rows[4]->getY() + 1);
}

TEST (CanvasView, TheEngineSaysWhereItRuns)
{
    EXPECT_EQ (catalog (1).front().caption, juce::String::fromUTF8 ("on the A³ Core"));
}

TEST (TileComponent, ARowPaintsItsNameAndVersion)
{
    LookAndFeel_Canvas look;
    TileComponent row (deckTile());
    row.setStatus (statusWith (Light::running), "03.0+281");
    const auto image = paintedTile (row, look);
    EXPECT_GT (pixelsUnlike (image, row.labelArea(), skin::surfaceRaised), 50);
    EXPECT_GT (pixelsUnlike (image, row.versionArea(), skin::surfaceRaised), 20);
    EXPECT_LT (row.versionArea().getRight(), row.startStopButton().getX() + 1) << "the version sits before the keys";
    row.setLookAndFeel (nullptr);
}

// -- The greeter -------------------------------------------------------------------

TEST (Greeter, TheLinksAreHyperlinksToTheirTargets)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    ASSERT_EQ (greeter.getLinks().size(), 3);
    const auto expected = greeterLinks();
    for (int i = 0; i < greeter.getLinks().size(); ++i)
    {
        EXPECT_EQ (greeter.getLinks()[i]->getButtonText(), expected[(size_t) i].label);
        EXPECT_EQ (greeter.getLinks()[i]->getURL().toString (false), expected[(size_t) i].url);
    }
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

TEST (Greeter, TheAboutBlockIsWrittenUnderTheLogo)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    EXPECT_GE (greeter.aboutArea().getY(), juce::roundToInt (greeter.logoArea().getBottom()));
    EXPECT_GT (pixelsUnlike (snapshotOf (greeter), greeter.aboutArea(), skin::surface), 300) << "copyright, contact, licences";
    EXPECT_TRUE (greeter.aboutArea().contains (greeter.licenceArea()));
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

TEST (Greeter, ThisMachinesAddressesAreWritten)
{
    LookedGreeter looked;
    auto& greeter = looked.greeter;
    greeter.setMachineLine (juce::String::fromUTF8 ("this machine · 192.168.8.10 · 192.168.9.10"));
    const auto image = snapshotOf (greeter);
    EXPECT_GT (pixelsUnlike (image, greeter.machineLineArea(), skin::surface), 100);
    EXPECT_EQ (pixelsNear (image, greeter.machineLineArea(), skin::textPrimary, 20), 0) << "muted";
    EXPECT_FALSE (greeter.machineLineArea().intersects (greeter.aboutArea()));
}

TEST (TileComponent, TheHostIsAMutedLineUnderTheName)
{
    LookAndFeel_Canvas look;
    TileComponent row (deckTile());
    row.setStatus (statusWith (Light::running), "03.0");
    row.setHost (juce::String::fromUTF8 ("local · 192.168.8.10"));
    const auto image = paintedTile (row, look);
    EXPECT_GE (row.hostArea().getY(), row.labelArea().getBottom() - 1) << "under the name";
    EXPECT_GT (pixelsUnlike (image, row.hostArea(), skin::surfaceRaised), 60);
    EXPECT_EQ (pixelsNear (image, row.hostArea(), skin::textPrimary, 20), 0) << "muted";
    EXPECT_LT (row.hostArea().getRight(), row.versionArea().getX() + 1);
    row.setLookAndFeel (nullptr);
}

TEST (CanvasWindow, TheDemoNamesTheTruthsAddresses)
{
    CanvasView view (catalog (4));
    auto setup = demoSetup (4);
    setup.truth = parseTruthNetwork (juce::JSON::parse (fixture ("truth-network.json")));
    CanvasController controller (view, std::move (setup));
    EXPECT_TRUE (view.greeter().getMachineLine().contains ("192.168.8.10"));
    EXPECT_TRUE (view.getTiles().front()->getHost().contains ("192.168.8.10")) << "the engine on the core";
}

// -- Support A³ ---------------------------------------------------------------------

TEST (Support, HiddenWhileNothingIsSet)
{
    LookedGreeter looked;
    EXPECT_FALSE (looked.greeter.supportCard().isVisible());
}

TEST (Support, ALinkPerSetUrlAndTheAddressWithItsCode)
{
    LookedGreeter looked (everySupport());
    auto& card = looked.greeter.supportCard();
    ASSERT_TRUE (card.isVisible());
    ASSERT_EQ (card.getLinks().size(), 2);
    EXPECT_EQ (card.getLinks()[0]->getButtonText(), "Ko-fi");
    EXPECT_EQ (card.getLinks()[0]->getURL().toString (false), "https://ko-fi.com/example");
    EXPECT_EQ (card.getLinks()[1]->getButtonText(), "PayPal");
    EXPECT_EQ (card.getLinks()[1]->getURL().toString (false), "https://paypal.me/example");
    EXPECT_TRUE (card.copyButton().isVisible());
    EXPECT_FALSE (card.qrArea().isEmpty());
}

TEST (Support, OnlyWhatIsSet)
{
    LookedGreeter looked (SupportConfig { {}, "https://paypal.me/example", {} });
    auto& card = looked.greeter.supportCard();
    ASSERT_TRUE (card.isVisible());
    ASSERT_EQ (card.getLinks().size(), 1);
    EXPECT_EQ (card.getLinks()[0]->getButtonText(), "PayPal");
    EXPECT_FALSE (card.copyButton().isVisible()) << "no address, nothing to copy";
    EXPECT_TRUE (card.qrArea().isEmpty()) << "and no code";
}

TEST (Support, TheCodeAndTheAddressPaint)
{
    LookedGreeter looked (everySupport());
    auto& card = looked.greeter.supportCard();
    const auto image = snapshotOf (card);
    const auto qr = card.qrArea().toNearestInt();
    EXPECT_GT (pixelsNear (image, qr, skin::textPrimary, 8), qr.getWidth() * qr.getHeight() / 5) << "the light ground";
    EXPECT_GT (pixelsNear (image, qr, skin::background, 8), qr.getWidth() * qr.getHeight() / 5) << "the dark modules";
    const auto finder = card.qrModuleCentre (3, 3).toInt();
    EXPECT_TRUE (near (image.getPixelAt (finder.x, finder.y), skin::background)) << "a finder pattern's centre is dark";
    EXPECT_GT (pixelsUnlike (image, card.addressArea(), skin::surfaceRaised), 100) << "the address is written";
}

TEST (Support, CopyHandsTheAddressOn)
{
    LookedGreeter looked (everySupport());
    auto& card = looked.greeter.supportCard();
    juce::String copied;
    card.copyText = [&] (const juce::String& text) { copied = text; };
    card.copyButton().triggerClick();
    pumpUntil ([&] { return copied.isNotEmpty(); });
    EXPECT_EQ (copied, exampleAddress);
}

TEST (CanvasWindow, TheDemoSaysItIsADemo)
{
    CanvasView view (catalog (4));
    CanvasController controller (view, demoSetup (4));
    EXPECT_TRUE (view.getSubtitle().startsWith ("Demo"));
    view.setSize (rigWidth, rigHeight);
    const auto image = snapshotOf (view);
    EXPECT_GT (pixelsUnlike (image, view.subtitleArea(), skin::surface), 100) << "and paints it";
    EXPECT_GT (pixelsNear (image, view.getLocalArea (&view.greeter(), view.greeter().versionsArea()), skin::textPrimary, 20), 100)
        << "the demo's versions";
}

namespace
{
// What every installation shows: the package's canvas.json.
SupportConfig shippedSupport()
{
    return loadSupport ({}, juce::File (A3CANVAS_FIXTURES).getChildFile ("../../packaging/canvas.json"));
}

// The demo as on a machine with the shipped truth (this one may have none).
CanvasSetup demoWithTheTruth()
{
    auto setup = demoSetup (4);
    setup.truth = parseTruthNetwork (juce::JSON::parse (fixture ("truth-network.json")));
    return setup;
}

void writePng (juce::Component& component, const juce::File& file)
{
    file.deleteFile();
    juce::FileOutputStream stream (file);
    ASSERT_TRUE (stream.openedOk());
    ASSERT_TRUE (juce::PNGImageFormat().writeImageToStream (snapshotOf (component), stream));
}
}

// For the maintainer's eye: with A3CANVAS_SNAPSHOT_DIR set, the demo at the rig's size as a PNG.
TEST (CanvasWindow, WritesTheRigSizedScreenForReview)
{
    const auto directory = juce::SystemStats::getEnvironmentVariable ("A3CANVAS_SNAPSHOT_DIR", {});
    if (directory.isEmpty())
        GTEST_SKIP() << "A3CANVAS_SNAPSHOT_DIR not set";
    CanvasView view (catalog (4), shippedSupport());
    CanvasController controller (view, demoWithTheTruth());
    view.setSize (rigWidth, rigHeight);
    view.appendLog ("-- Start all");
    for (const auto& command : startAll (catalog (4), "/home/dj/.config/a3/laptop/a3-osc.json"))
        view.appendLog ("$ " + command.argv.joinIntoString (" "));
    view.appendLog ("Start all: done");
    ASSERT_TRUE (juce::File (directory).createDirectory().wasOk());
    writePng (view, juce::File (directory).getChildFile ("a3-canvas.png"));

    view.setSize (1920, 1080);
    writePng (view, juce::File (directory).getChildFile ("a3-canvas-laptop.png"));

    // With every support entry set to an example (not a real target), for the layout's sake.
    CanvasView supported (catalog (4), everySupport());
    CanvasController supportedController (supported, demoWithTheTruth());
    supported.setSize (rigWidth, rigHeight);
    writePng (supported, juce::File (directory).getChildFile ("a3-canvas-support-example.png"));
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
