// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>
#include <juce_events/juce_events.h>

int main (int argc, char** argv)
{
    ::testing::InitGoogleTest (&argc, argv);
    // This thread is the message thread: the paint tests run on it, synchronously.
    juce::ScopedJuceInitialiser_GUI juce;
    return RUN_ALL_TESTS();
}
