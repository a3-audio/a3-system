// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "Fixtures.h"
#include "sys/CoreProbe.h"

using namespace canvas;

TEST (CoreProbe, TheRigNamesThePresentDecks)
{
    const auto core = parseRig (fixture ("core-rig.json"));
    EXPECT_TRUE (core.reachable);
    EXPECT_EQ (core.presentDecks, (std::set<int> { 1, 2 }));
    EXPECT_TRUE (core.engineHeard);
}

TEST (CoreProbe, NoAnswerIsUnreachable)
{
    EXPECT_FALSE (parseRig ({}).reachable);
    EXPECT_FALSE (parseRig ("<html>502</html>").reachable);
}

TEST (CoreProbe, TheEngineStatusSaysRateBlockAndLoad)
{
    const auto engine = parseEngineStatus (fixture ("engine-status.json"));
    EXPECT_TRUE (engine.answers);
    EXPECT_TRUE (engine.running());
    EXPECT_EQ (engine.sampleRate, 48000);
    EXPECT_EQ (engine.blockSize, 256);
    EXPECT_FLOAT_EQ (engine.dspLoadPercent, 11.5f);
    EXPECT_EQ (engine.xruns, 0);
}

TEST (CoreProbe, AnEngineWithAProblemIsNotRunning)
{
    auto json = juce::JSON::parse (fixture ("engine-status.json"));
    json.getDynamicObject()->setProperty ("engineProblem", "port taken: system:playback_1");
    const auto engine = parseEngineStatus (juce::JSON::toString (json));
    EXPECT_TRUE (engine.answers);
    EXPECT_FALSE (engine.running());
    EXPECT_EQ (engine.problem, "port taken: system:playback_1");
}

TEST (CoreProbe, NoEngineAnswerIsNotRunning)
{
    const auto engine = parseEngineStatus ({});
    EXPECT_FALSE (engine.answers);
    EXPECT_FALSE (engine.running());
}
