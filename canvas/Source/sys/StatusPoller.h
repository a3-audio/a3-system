// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <functional>
#include <mutex>

#include <juce_events/juce_events.h>

#include "model/TileStatus.h"
#include "sys/CommandRunner.h"

namespace canvas
{
// GET a URL; the body, or empty when nothing answered in time.
using HttpGet = std::function<juce::String (const juce::String& url)>;

// juce::URL with a short connection timeout, for Core and the engine on this machine.
juce::String httpGetLocal (const juce::String& url);

struct Snapshot
{
    Facts facts;
    std::vector<TileStatus> statuses;   // one per tile, in the catalog's order
};

// Asks systemd, dpkg, Core and the engine once a period on a thread of its own, and hands each
// snapshot to the message thread; the message thread never waits for a command or a socket.
class StatusPoller : private juce::Thread, private juce::AsyncUpdater
{
public:
    StatusPoller (std::vector<Tile> tiles, CommandRunner& runner, HttpGet http, int periodMs = 1000);
    ~StatusPoller() override;

    // Called on the message thread with the newest snapshot.
    std::function<void (const Snapshot&)> onSnapshot;
    // This machine's addresses and the truth's hosts, asked each poll; set before start().
    std::function<NetworkFacts()> networkFacts;

    void start();
    void stop();

    // One poll, on the calling thread.
    Snapshot pollOnce();

private:
    void run() override;
    void handleAsyncUpdate() override;

    const std::vector<Tile> tiles;
    CommandRunner& runner;
    const HttpGet http;
    const int periodMs;

    std::map<juce::String, PackageFacts> policy;
    juce::uint32 policyAskedAt = 0;
    bool policyAsked = false;

    std::mutex latestLock;
    Snapshot latest;
};
}
