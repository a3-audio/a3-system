// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Support.h"

#include <qrcodegen.hpp>

namespace canvas
{
namespace
{
const juce::String base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
const juce::String bech32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";

// https://<one of hosts>/<a path without spaces>, nothing else.
bool isLinkTo (const juce::String& text, std::initializer_list<const char*> hosts)
{
    if (! text.startsWith ("https://") || text.containsAnyOf (" \t\r\n\"'<>"))
        return false;
    const auto rest = text.fromFirstOccurrenceOf ("https://", false, false);
    const auto host = rest.upToFirstOccurrenceOf ("/", false, false).toLowerCase();
    const auto path = rest.fromFirstOccurrenceOf ("/", false, false);
    if (path.isEmpty() || ! rest.containsChar ('/'))
        return false;
    for (const auto* allowed : hosts)
        if (host == allowed)
            return true;
    return false;
}

// The address's form only (prefix, alphabet, length); the checksum is the wallet's to check.
bool isBitcoinAddress (const juce::String& text)
{
    if (text.startsWith ("bc1"))
        return text.length() >= 14 && text.length() <= 90 && text.substring (3).containsOnly (bech32);
    return (text.startsWithChar ('1') || text.startsWithChar ('3')) && text.length() >= 26 && text.length() <= 35
           && text.containsOnly (base58);
}

juce::String entry (const juce::var& json, const char* key)
{
    const auto value = json.getProperty (key, {});
    return value.isString() ? value.toString().trim() : juce::String();
}

juce::File home() { return juce::File::getSpecialLocation (juce::File::userHomeDirectory); }
}

SupportConfig parseSupport (const juce::String& jsonText)
{
    const auto json = juce::JSON::parse (jsonText);
    if (! json.isObject())
        return {};
    SupportConfig support;
    if (const auto kofi = entry (json, "kofi"); isLinkTo (kofi, { "ko-fi.com", "www.ko-fi.com" }))
        support.kofi = kofi;
    if (const auto paypal = entry (json, "paypal"); isLinkTo (paypal, { "paypal.me", "www.paypal.me" }))
        support.paypal = paypal;
    if (const auto bitcoin = entry (json, "bitcoin"); isBitcoinAddress (bitcoin))
        support.bitcoin = bitcoin;
    return support;
}

SupportConfig loadSupport (const juce::File& user, const juce::File& shipped)
{
    if (user.existsAsFile())
        return parseSupport (user.loadFileAsString());
    if (shipped.existsAsFile())
        return parseSupport (shipped.loadFileAsString());
    return {};
}

SupportConfig machineSupport()
{
    return loadSupport (home().getChildFile (".config/a3/canvas.json"), juce::File ("/usr/share/a3/canvas.json"));
}

juce::String bitcoinUri (const juce::String& address)
{
    if (address.startsWith ("bc1"))
        return ("bitcoin:" + address).toUpperCase();
    return "bitcoin:" + address;
}

std::vector<std::vector<bool>> qrModules (const juce::String& text)
{
    const auto code = qrcodegen::QrCode::encodeText (text.toRawUTF8(), qrcodegen::QrCode::Ecc::MEDIUM);
    std::vector<std::vector<bool>> rows (static_cast<size_t> (code.getSize()));
    for (int y = 0; y < code.getSize(); ++y)
        for (int x = 0; x < code.getSize(); ++x)
            rows[(size_t) y].push_back (code.getModule (x, y));
    return rows;
}
}
