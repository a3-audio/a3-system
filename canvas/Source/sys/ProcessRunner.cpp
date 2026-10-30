// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "CommandRunner.h"

namespace canvas
{
int ProcessRunner::run (const juce::StringArray& argv, const LineCallback& line)
{
    juce::ChildProcess process;
    if (! process.start (argv, juce::ChildProcess::wantStdOut | juce::ChildProcess::wantStdErr))
    {
        if (line)
            line (argv[0] + ": could not be started");
        return -1;
    }
    // Lines as they come, so a long job's log streams; a partial line waits for its end.
    juce::String pending;
    char buffer[4096];
    for (;;)
    {
        const int got = process.readProcessOutput (buffer, sizeof (buffer));
        if (got <= 0)
            break;
        pending += juce::String::fromUTF8 (buffer, got);
        while (pending.containsChar ('\n'))
        {
            if (line)
                line (pending.upToFirstOccurrenceOf ("\n", false, false));
            pending = pending.fromFirstOccurrenceOf ("\n", false, false);
        }
    }
    if (line && pending.isNotEmpty())
        line (pending);
    process.waitForProcessToFinish (-1);
    return static_cast<int> (process.getExitCode());
}
}
