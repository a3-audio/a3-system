// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <map>
#include <mutex>

#include "sys/CommandRunner.h"

// Records every command and answers from a table: no test runs systemctl, apt or pkexec.
class FakeRunner : public canvas::CommandRunner
{
public:
    // Exit code and output for a command line (argv joined by spaces); anything else exits 0, silent.
    void answer (const juce::String& commandLine, int exitCode, const juce::String& output = {})
    {
        const std::lock_guard<std::mutex> guard (lock);
        answers[commandLine] = { exitCode, output };
    }

    int run (const juce::StringArray& argv, const LineCallback& line) override
    {
        const auto commandLine = argv.joinIntoString (" ");
        Answer reply;
        {
            const std::lock_guard<std::mutex> guard (lock);
            ran.add (commandLine);
            if (const auto found = answers.find (commandLine); found != answers.end())
                reply = found->second;
        }
        if (line)
            for (const auto& text : juce::StringArray::fromLines (reply.output))
                if (text.isNotEmpty())
                    line (text);
        return reply.exitCode;
    }

    juce::StringArray commands() const
    {
        const std::lock_guard<std::mutex> guard (lock);
        return ran;
    }

private:
    struct Answer
    {
        int exitCode = 0;
        juce::String output;
    };
    mutable std::mutex lock;
    std::map<juce::String, Answer> answers;
    juce::StringArray ran;
};
