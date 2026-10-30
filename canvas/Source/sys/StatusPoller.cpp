// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "StatusPoller.h"

namespace canvas
{
namespace
{
const juce::String rigUrl = "http://127.0.0.1:9080/api/rig";
const juce::String engineUrl = "http://127.0.0.1:9005/api/engine/status";
// Both answer on this machine at once or not at all; a longer wait only delays the units' news.
constexpr int httpTimeoutMs = 300;
// apt-cache policy reads the whole package cache; versions change on an update, not by the second.
constexpr juce::uint32 policyPeriodMs = 30000;

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
}

juce::String httpGetLocal (const juce::String& url)
{
    int status = 0;
    const auto options = juce::URL::InputStreamOptions (juce::URL::ParameterHandling::inAddress)
                             .withConnectionTimeoutMs (httpTimeoutMs)
                             .withStatusCode (&status);
    const auto stream = juce::URL (url).createInputStream (options);
    if (stream == nullptr || status != 200)
        return {};
    return stream->readEntireStreamAsString();
}

StatusPoller::StatusPoller (std::vector<Tile> tilesToShow, CommandRunner& runnerToUse, HttpGet httpToUse, int period)
    : juce::Thread ("a3-canvas status"), tiles (std::move (tilesToShow)), runner (runnerToUse),
      http (std::move (httpToUse)), periodMs (period)
{
}

StatusPoller::~StatusPoller()
{
    stop();
    cancelPendingUpdate();
}

void StatusPoller::start()
{
    startThread();
}

void StatusPoller::stop()
{
    signalThreadShouldExit();
    notify();
    stopThread (2000);
}

Snapshot StatusPoller::pollOnce()
{
    const auto packages = packagesOf (tiles);
    const auto now = juce::Time::getMillisecondCounter();
    if (! policyAsked || now - policyAskedAt >= policyPeriodMs)
    {
        policy = parseAptPolicy (outputOf (runner, aptPolicyCommand (packages)));
        policyAskedAt = now;
        policyAsked = true;
    }

    Snapshot snapshot;
    snapshot.facts.units = parseSystemctlShow (outputOf (runner, showCommand (unitsOf (tiles))));
    snapshot.facts.packages = packageFacts (parseDpkgQuery (outputOf (runner, dpkgQueryCommand (packages))), policy, packages);
    snapshot.facts.core = parseRig (http (rigUrl));
    snapshot.facts.engine = parseEngineStatus (http (engineUrl));
    if (networkFacts)
        snapshot.facts.network = networkFacts();
    for (const auto& tile : tiles)
        snapshot.statuses.push_back (statusOf (tile, snapshot.facts));
    return snapshot;
}

void StatusPoller::run()
{
    while (! threadShouldExit())
    {
        auto snapshot = pollOnce();
        {
            const std::lock_guard<std::mutex> guard (latestLock);
            latest = std::move (snapshot);
        }
        triggerAsyncUpdate();
        wait (periodMs);
    }
}

void StatusPoller::handleAsyncUpdate()
{
    Snapshot snapshot;
    {
        const std::lock_guard<std::mutex> guard (latestLock);
        snapshot = latest;
    }
    if (onSnapshot)
        onSnapshot (snapshot);
}
}
