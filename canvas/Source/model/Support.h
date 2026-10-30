// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <vector>

#include <juce_core/juce_core.h>

namespace canvas
{
// Where "Support A³" leads, from ~/.config/a3/canvas.json or the package's default (all empty).
// An entry that is not what its key says is dropped, so nobody is sent to a mistyped target.
struct SupportConfig
{
    juce::String kofi;      // https://ko-fi.com/<name>
    juce::String paypal;    // https://paypal.me/<name>
    juce::String bitcoin;   // an address (1…, 3… or bc1…)

    bool isEmpty() const { return kofi.isEmpty() && paypal.isEmpty() && bitcoin.isEmpty(); }
};

SupportConfig parseSupport (const juce::String& jsonText);
// The user's file when it exists (whole, not merged), else the shipped one, else nothing.
SupportConfig loadSupport (const juce::File& user, const juce::File& shipped);
SupportConfig machineSupport();

// BIP 21: what a wallet's camera expects in the code.
juce::String bitcoinUri (const juce::String& address);
// The QR code's modules, row by row, true for dark; without the quiet zone.
std::vector<std::vector<bool>> qrModules (const juce::String& text);
}
