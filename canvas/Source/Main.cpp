// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <juce_gui_basics/juce_gui_basics.h>

#include "ui/CanvasWindow.h"

namespace
{
constexpr int demoDecks = 4;
}

class CanvasApp : public juce::JUCEApplication
{
public:
    const juce::String getApplicationName() override { return juce::String::fromUTF8 ("A³ Canvas"); }
    const juce::String getApplicationVersion() override { return JUCE_APPLICATION_VERSION_STRING; }
    bool moreThanOneInstanceAllowed() override { return false; }

    // --demo: a made-up rig that runs nothing, for pictures and for trying the window.
    void initialise (const juce::String& commandLine) override
    {
        const bool demo = juce::StringArray::fromTokens (commandLine, true).contains ("--demo");
        window = std::make_unique<canvas::CanvasWindow> (demo ? canvas::demoSetup (demoDecks) : canvas::machineSetup());
        window->setVisible (true);
    }

    void shutdown() override { window = nullptr; }
    void systemRequestedQuit() override { quit(); }

private:
    std::unique_ptr<canvas::CanvasWindow> window;
};

START_JUCE_APPLICATION (CanvasApp)
