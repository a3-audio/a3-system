// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "model/Support.h"

using namespace canvas;

namespace
{
// BIP 173's own example address: valid in form, nobody's wallet.
const juce::String exampleBech32 = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4";
const juce::String exampleBase58 = "1BoatSLRHtKNngkdXEeobR76b53LETtpyT";

struct TempDir
{
    juce::File dir = juce::File::createTempFile ("a3-canvas-support");
    TempDir() { dir.createDirectory(); }
    ~TempDir() { dir.deleteRecursively(); }
};
}

TEST (Support, AllThreeWhenAllAreValid)
{
    const auto support = parseSupport (R"({ "kofi": "https://ko-fi.com/someone",
                                            "paypal": "https://paypal.me/someone",
                                            "bitcoin": ")" + exampleBech32 + "\" }");
    EXPECT_EQ (support.kofi, "https://ko-fi.com/someone");
    EXPECT_EQ (support.paypal, "https://paypal.me/someone");
    EXPECT_EQ (support.bitcoin, exampleBech32);
    EXPECT_FALSE (support.isEmpty());
}

TEST (Support, TheShippedDefaultIsAllEmpty)
{
    const auto support = parseSupport (R"({ "kofi": "", "paypal": "", "bitcoin": "" })");
    EXPECT_TRUE (support.isEmpty());
}

TEST (Support, APartialFileGivesWhatItHas)
{
    const auto support = parseSupport (R"({ "paypal": "https://www.paypal.me/someone" })");
    EXPECT_TRUE (support.kofi.isEmpty());
    EXPECT_EQ (support.paypal, "https://www.paypal.me/someone");
    EXPECT_TRUE (support.bitcoin.isEmpty());
    EXPECT_FALSE (support.isEmpty());
}

TEST (Support, AnInvalidEntryIsRefusedAndTheRestKept)
{
    const auto support = parseSupport (R"({ "kofi": "http://ko-fi.com/someone",
                                            "paypal": "https://evil.example/paypal.me/x",
                                            "bitcoin": ")" + exampleBase58 + "\" }");
    EXPECT_TRUE (support.kofi.isEmpty()) << "plain http is refused";
    EXPECT_TRUE (support.paypal.isEmpty()) << "only paypal.me";
    EXPECT_EQ (support.bitcoin, exampleBase58);
}

TEST (Support, WhatIsNotALinkOrAnAddressIsRefused)
{
    for (const auto* kofi : { "ko-fi.com/someone", "https://ko-fi.com/", "https://ko-fi.com/a b", "https://ko-fi.com.evil.example/x", "javascript:alert(1)" })
        EXPECT_TRUE (parseSupport (juce::String ("{ \"kofi\": \"") + kofi + "\" }").kofi.isEmpty()) << kofi;
    for (const auto* bitcoin : { "bc1", "not an address", "0BoatSLRHtKNngkdXEeobR76b53LETtpyT", "1BoatSLRHtKNngkdXEeobR76b53LETtpyI" /* I is not base58 */ })
        EXPECT_TRUE (parseSupport (juce::String ("{ \"bitcoin\": \"") + bitcoin + "\" }").bitcoin.isEmpty()) << bitcoin;
}

TEST (Support, NotJsonIsEmpty)
{
    EXPECT_TRUE (parseSupport ("kofi = https://ko-fi.com/x").isEmpty());
    EXPECT_TRUE (parseSupport ({}).isEmpty());
    EXPECT_TRUE (parseSupport ("[1, 2]").isEmpty());
}

TEST (Support, TheUsersFileBeforeTheShippedOne)
{
    TempDir temp;
    const auto user = temp.dir.getChildFile ("user.json");
    const auto shipped = temp.dir.getChildFile ("shipped.json");
    ASSERT_TRUE (shipped.replaceWithText (R"({ "kofi": "https://ko-fi.com/shipped" })"));
    EXPECT_EQ (loadSupport (user, shipped).kofi, "https://ko-fi.com/shipped") << "no user file: the shipped one";
    ASSERT_TRUE (user.replaceWithText (R"({ "paypal": "https://paypal.me/mine" })"));
    const auto mine = loadSupport (user, shipped);
    EXPECT_TRUE (mine.kofi.isEmpty()) << "the user's file replaces the shipped one, it does not merge";
    EXPECT_EQ (mine.paypal, "https://paypal.me/mine");
}

TEST (Support, NoFileAtAllIsEmpty)
{
    TempDir temp;
    EXPECT_TRUE (loadSupport (temp.dir.getChildFile ("a.json"), temp.dir.getChildFile ("b.json")).isEmpty());
}

TEST (Support, TheBitcoinQrCodeCarriesAPaymentUri)
{
    // BIP 173: a bech32 address goes into a code in upper case (the smaller alphanumeric mode);
    // BIP 21's scheme is case-blind. A base58 address keeps its case: it is part of the address.
    EXPECT_EQ (bitcoinUri (exampleBech32), "BITCOIN:" + exampleBech32.toUpperCase());
    EXPECT_EQ (bitcoinUri (exampleBase58), "bitcoin:" + exampleBase58);
    const auto modules = qrModules (bitcoinUri (exampleBech32));
    ASSERT_GE (modules.size(), 21u) << "version 1 or larger";
    for (const auto& row : modules)
        EXPECT_EQ (row.size(), modules.size()) << "square";
    // The three finder patterns: a dark 7 × 7 frame in three corners.
    const auto n = modules.size();
    for (const auto& corner : { std::pair<size_t, size_t> { 0, 0 }, { 0, n - 7 }, { n - 7, 0 } })
    {
        EXPECT_TRUE (modules[corner.first][corner.second]);
        EXPECT_TRUE (modules[corner.first + 6][corner.second + 6]);
        EXPECT_FALSE (modules[corner.first + 1][corner.second + 1]) << "the light ring";
        EXPECT_TRUE (modules[corner.first + 3][corner.second + 3]) << "the dark centre";
    }
}
