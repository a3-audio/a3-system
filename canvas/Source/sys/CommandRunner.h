// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <functional>

#include <juce_core/juce_core.h>

namespace canvas
{
// Runs one command, no shell; every line of its output (stdout and stderr) goes to `line`.
// Returns the exit code, or -1 when it could not be started. The app uses ProcessRunner;
// tests use a fake, so no test ever runs systemctl, apt or pkexec.
class CommandRunner
{
public:
    using LineCallback = std::function<void (const juce::String&)>;

    virtual ~CommandRunner() = default;
    virtual int run (const juce::StringArray& argv, const LineCallback& line) = 0;
};

// The whole output of a command, or empty when it exited with an error and printed nothing useful.
inline juce::String outputOf (CommandRunner& runner, const juce::StringArray& argv)
{
    juce::StringArray lines;
    runner.run (argv, [&lines] (const juce::String& text) { lines.add (text); });
    return lines.joinIntoString ("\n");
}

class ProcessRunner : public CommandRunner
{
public:
    int run (const juce::StringArray& argv, const LineCallback& line) override;
};
}
