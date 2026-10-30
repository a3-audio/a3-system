// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "model/AppCatalog.h"

using namespace canvas;

namespace
{
std::vector<juce::String> idsOf (const std::vector<Tile>& tiles)
{
    std::vector<juce::String> ids;
    for (const auto& tile : tiles)
        ids.push_back (tile.id);
    return ids;
}

const Tile& tileWithId (const std::vector<Tile>& tiles, const juce::String& id)
{
    for (const auto& tile : tiles)
        if (tile.id == id)
            return tile;
    throw std::out_of_range (id.toStdString());
}
}

// Plan R2 plus the beat-analyzer as a tile of its own (it is a program the rig runs).
TEST (Catalog, FourDecksMakeEightTiles)
{
    const auto tiles = catalog (4);
    const std::vector<juce::String> expected { "core", "deck-A", "deck-B", "deck-C", "deck-D", "mixer", "motion", "analyzer" };
    EXPECT_EQ (idsOf (tiles), expected);
}

TEST (Catalog, TheUnitsAreTheOnesThePackagesShip)
{
    const auto tiles = catalog (2);
    const auto& core = tileWithId (tiles, "core");
    EXPECT_EQ (core.units, (std::vector<juce::String> { "a3-engine.service", "a3-core.service", "a3-core-window.service" }));
    EXPECT_EQ (core.package, "a3-core-app");
    EXPECT_EQ (core.windowUnit, "a3-core-window.service");

    const auto& deckB = tileWithId (tiles, "deck-B");
    EXPECT_EQ (deckB.kind, TileKind::deck);
    EXPECT_EQ (deckB.units, (std::vector<juce::String> { "stemdeck@B.service" }));
    EXPECT_EQ (deckB.package, "stemdeck");
    EXPECT_EQ (deckB.deck, 2);

    EXPECT_EQ (tileWithId (tiles, "mixer").units, (std::vector<juce::String> { "a3-desk.service" }));
    EXPECT_EQ (tileWithId (tiles, "mixer").package, "a3-desk");
    EXPECT_EQ (tileWithId (tiles, "motion").units, (std::vector<juce::String> { "a3-motion.service" }));
    EXPECT_EQ (tileWithId (tiles, "motion").package, "a3-motion-ui");
    EXPECT_EQ (tileWithId (tiles, "analyzer").units, (std::vector<juce::String> { "beat-analyzer.service" }));
    EXPECT_EQ (tileWithId (tiles, "analyzer").package, "beat-analyzer");
}

TEST (Catalog, EveryTileHasALabel)
{
    for (const auto& tile : catalog (4))
        EXPECT_TRUE (tile.label.isNotEmpty()) << tile.id;
    EXPECT_EQ (tileWithId (catalog (4), "deck-C").label, "Deck C");
}

TEST (Catalog, LettersMatchTheInstaller)
{
    EXPECT_EQ (deckLetters (1), (std::vector<juce::String> { "A" }));
    EXPECT_EQ (deckLetters (26).back(), "Z");
    EXPECT_EQ (deckLetters (27).back(), "AA");
    EXPECT_EQ (deckLetters (28).back(), "AB");
    EXPECT_EQ (deckLetters (53).back(), "BA");
    EXPECT_TRUE (deckLetters (0).empty());
}

TEST (Catalog, EmptyDecksSettingTakesTheTruth)
{
    EXPECT_EQ (decksFromInstallConf ("[laptop]\ndecks =\noutput_main = 1,2\n", 4), 4);
    EXPECT_EQ (decksFromInstallConf ("", 4), 4);
    EXPECT_EQ (decksFromInstallConf ("[core]\ndecks = 2\n", 4), 4);
}

TEST (Catalog, ADecksSettingIsTaken)
{
    EXPECT_EQ (decksFromInstallConf ("[general]\nroles = laptop\n\n[laptop]\ndecks = 3\n", 4), 3);
    EXPECT_EQ (decksFromInstallConf ("[laptop]\n  decks=2  \n", 4), 2);
}

// The installer refuses such a setting; the Canvas shows what the installer can have made.
TEST (Catalog, ASettingTheInstallerRefusesFallsBackToTheTruth)
{
    EXPECT_EQ (decksFromInstallConf ("[laptop]\ndecks = 9\n", 4), 4);
    EXPECT_EQ (decksFromInstallConf ("[laptop]\ndecks = 0\n", 4), 4);
    EXPECT_EQ (decksFromInstallConf ("[laptop]\ndecks = two\n", 4), 4);
}

TEST (Catalog, TheTruthsDeckRangeIsTheDeckHellosUpperBound)
{
    const auto truth = juce::JSON::parse (R"({"addresses": {"stemdeck.deck-hello": {"deck": [1, 6]}}})");
    EXPECT_EQ (truthDeckCount (truth, 4), 6);
    EXPECT_EQ (truthDeckCount (juce::var(), 4), 4);
    EXPECT_EQ (truthDeckCount (juce::JSON::parse (R"({"addresses": {}})"), 4), 4);
}
