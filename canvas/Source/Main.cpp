// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <juce_gui_basics/juce_gui_basics.h>

class CanvasApp : public juce::JUCEApplication
{
public:
    const juce::String getApplicationName() override { return "A³ Canvas"; }
    const juce::String getApplicationVersion() override { return JUCE_APPLICATION_VERSION_STRING; }
    bool moreThanOneInstanceAllowed() override { return false; }

    void initialise (const juce::String&) override
    {
        window = std::make_unique<juce::DocumentWindow> (juce::String::fromUTF8 ("A³ Canvas"), juce::Colours::black,
                                                         juce::DocumentWindow::allButtons);
        window->setUsingNativeTitleBar (true);
        window->centreWithSize (800, 600);
        window->setVisible (true);
    }

    void shutdown() override { window = nullptr; }
    void systemRequestedQuit() override { quit(); }

private:
    std::unique_ptr<juce::DocumentWindow> window;
};

START_JUCE_APPLICATION (CanvasApp)
