// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "AppCatalog.h"

#include "model/Ini.h"

namespace canvas
{
namespace
{
juce::String deckLetter (int number)
{
    juce::String letters;
    while (number > 0)
    {
        const int rest = (number - 1) % 26;
        number = (number - 1) / 26;
        letters = juce::String::charToString (static_cast<juce::juce_wchar> ('A' + rest)) + letters;
    }
    return letters;
}

Tile deckTile (int deck, const juce::String& letter)
{
    const auto unit = "stemdeck@" + letter + ".service";
    return { TileKind::deck, "deck-" + letter, "Deck " + letter, "StemDeck", { unit }, "stemdeck", unit, deck };
}
}

std::vector<juce::String> deckLetters (int count)
{
    std::vector<juce::String> letters;
    for (int number = 1; number <= count; ++number)
        letters.push_back (deckLetter (number));
    return letters;
}

std::vector<Tile> catalog (int decks)
{
    std::vector<Tile> tiles;
    tiles.push_back ({ TileKind::core, "core", juce::String::fromUTF8 ("A³ Engine"),
                       juce::String::fromUTF8 ("on the A³ Core"),
                       { "a3-engine.service", "a3-core.service", "a3-core-window.service" },
                       "a3-core-app", "a3-core-window.service" });
    const auto letters = deckLetters (decks);
    for (size_t i = 0; i < letters.size(); ++i)
        tiles.push_back (deckTile (static_cast<int> (i) + 1, letters[i]));
    tiles.push_back ({ TileKind::mixer, "mixer", juce::String::fromUTF8 ("A³ Mixer"), "Desk",
                       { "a3-desk.service" }, "a3-desk", "a3-desk.service" });
    tiles.push_back ({ TileKind::motion, "motion", juce::String::fromUTF8 ("A³ Motion"), "Motion UI",
                       { "a3-motion.service" }, "a3-motion-ui", "a3-motion.service" });
    tiles.push_back ({ TileKind::analyzer, "analyzer", "Beat analyzer", "Beat clock",
                       { "beat-analyzer.service" }, "beat-analyzer", {} });
    return tiles;
}

int decksFromInstallConf (const juce::String& iniText, int truthDecks)
{
    const auto value = iniValue (iniText, "laptop", "decks");
    if (value.isEmpty() || ! value.containsOnly ("0123456789"))
        return truthDecks;
    const int wanted = value.getIntValue();
    return wanted >= 1 && wanted <= truthDecks ? wanted : truthDecks;
}

int truthDeckCount (const juce::var& truth, int fallback)
{
    const auto range = truth["addresses"]["stemdeck.deck-hello"]["deck"];
    if (! range.isArray() || range.size() != 2)
        return fallback;
    const int upper = static_cast<int> (range[1]);
    return upper >= 1 ? upper : fallback;
}
}
