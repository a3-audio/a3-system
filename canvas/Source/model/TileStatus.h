// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/AppCatalog.h"
#include "model/Network.h"
#include "model/System.h"
#include "sys/CoreProbe.h"
#include "sys/Packages.h"
#include "sys/Systemd.h"

namespace canvas
{
enum class Light { missing, stopped, starting, running, degraded, failed };

// Everything one poll learns about the machine.
struct Facts
{
    std::map<juce::String, UnitFacts> units;
    std::map<juce::String, PackageFacts> packages;
    CoreFacts core;
    EngineFacts engine;
    NetworkFacts network;
    SystemFacts system;                 // the system version this machine runs (the umbrella's pins)
    juce::String flashedMotionFirmware; // what the installer last flashed onto the Motion panel here
};

struct TileStatus
{
    Light light = Light::missing;
    juce::String line;
    bool updateAvailable = false;
    int windowPid = 0;
};

// Package not installed → missing; any unit failed → failed; any activating → starting; all active →
// running, unless Core does not hear a deck (degraded) or the engine does not answer (degraded);
// some active → degraded; none → stopped.
TileStatus statusOf (const Tile& tile, const Facts& facts);
}
