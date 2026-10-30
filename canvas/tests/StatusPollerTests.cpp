// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <atomic>

#include <gtest/gtest.h>
#include <juce_events/juce_events.h>

#include "FakeRunner.h"
#include "Fixtures.h"
#include "sys/StatusPoller.h"

using namespace canvas;

namespace
{
const juce::String rigUrl = "http://127.0.0.1:9080/api/rig";
const juce::String engineUrl = "http://127.0.0.1:9005/api/engine/status";

std::vector<juce::String> unitsOf (const std::vector<Tile>& tiles)
{
    std::vector<juce::String> units;
    for (const auto& tile : tiles)
        units.insert (units.end(), tile.units.begin(), tile.units.end());
    return units;
}

std::vector<juce::String> packagesOf (const std::vector<Tile>& tiles)
{
    std::vector<juce::String> packages;
    for (const auto& tile : tiles)
        if (std::find (packages.begin(), packages.end(), tile.package) == packages.end())
            packages.push_back (tile.package);
    return packages;
}

// A machine with everything installed and running, Core and the engine answering.
struct RunningRig
{
    std::vector<Tile> tiles = catalog (2);
    FakeRunner runner;
    std::atomic<int> httpCalls { 0 };
    bool coreAnswers = true;

    RunningRig()
    {
        juce::String show, dpkg;
        for (const auto& unit : unitsOf (tiles))
            show << "Id=" << unit << "\nLoadState=loaded\nActiveState=active\nSubState=running\nMainPID=100\nResult=success\n\n";
        for (const auto& package : packagesOf (tiles))
            dpkg << package << "\t1.0\tii \n";
        runner.answer (showCommand (unitsOf (tiles)).joinIntoString (" "), 0, show);
        runner.answer (dpkgQueryCommand (packagesOf (tiles)).joinIntoString (" "), 0, dpkg);
    }

    HttpGet http()
    {
        return [this] (const juce::String& url) -> juce::String {
            ++httpCalls;
            if (! coreAnswers)
                return {};
            if (url == rigUrl)
                return fixture ("core-rig.json");
            if (url == engineUrl)
                return fixture ("engine-status.json");
            return {};
        };
    }
};
}

TEST (StatusPoller, OnePollAsksSystemdDpkgCoreAndTheEngine)
{
    RunningRig rig;
    StatusPoller poller (rig.tiles, rig.runner, rig.http());
    const auto snapshot = poller.pollOnce();
    ASSERT_EQ (snapshot.statuses.size(), rig.tiles.size());
    EXPECT_EQ (snapshot.statuses[0].light, Light::running);
    EXPECT_TRUE (snapshot.facts.core.reachable);
    EXPECT_TRUE (snapshot.facts.engine.answers);
    EXPECT_EQ (rig.httpCalls.load(), 2);
}

TEST (StatusPoller, AnUnreachableCoreIsNotAnError)
{
    RunningRig rig;
    rig.coreAnswers = false;
    StatusPoller poller (rig.tiles, rig.runner, rig.http());
    const auto snapshot = poller.pollOnce();
    EXPECT_FALSE (snapshot.facts.core.reachable);
    EXPECT_FALSE (snapshot.facts.engine.answers);
    EXPECT_EQ (snapshot.statuses[0].light, Light::degraded);
    EXPECT_EQ (snapshot.statuses[1].light, Light::running) << "a deck is not degraded by Core's silence";
    // And the next poll still happens.
    EXPECT_NO_THROW (poller.pollOnce());
}

// apt-cache policy reads the whole package cache: not every second.
TEST (StatusPoller, ThePolicyIsAskedOnlyNowAndThen)
{
    RunningRig rig;
    StatusPoller poller (rig.tiles, rig.runner, rig.http());
    for (int i = 0; i < 5; ++i)
        poller.pollOnce();
    int policies = 0;
    for (const auto& line : rig.runner.commands())
        policies += line.startsWith ("apt-cache policy") ? 1 : 0;
    EXPECT_EQ (policies, 1);
}

TEST (StatusPoller, TheThreadDeliversOnTheMessageThread)
{
    RunningRig rig;
    StatusPoller poller (rig.tiles, rig.runner, rig.http(), 20);
    std::atomic<int> delivered { 0 };
    bool onMessageThread = true;
    poller.onSnapshot = [&] (const Snapshot&) {
        onMessageThread = onMessageThread && juce::MessageManager::getInstance()->isThisTheMessageThread();
        ++delivered;
    };
    rig.coreAnswers = false;
    poller.start();
    for (int i = 0; i < 100 && delivered < 2; ++i)
        juce::MessageManager::getInstance()->runDispatchLoopUntil (20);
    poller.stop();
    EXPECT_GE (delivered.load(), 2) << "the poller keeps running when Core does not answer";
    EXPECT_TRUE (onMessageThread);
}
