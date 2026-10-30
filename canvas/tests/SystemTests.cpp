// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later

#include <gtest/gtest.h>

#include "FakeRunner.h"
#include "Fixtures.h"
#include "model/System.h"
#include "sys/SystemRepo.h"

using namespace canvas;

namespace
{
const juce::String repo = "/home/dj/a3-system";
const juce::String motionPin = "abb88ad630e1159b268d5963c3131b4a3aba7c82";
const juce::String mixerPin = "16f805a2ec2efc43912751daf3b1c7169e4194ad";
const juce::String corePin = "747f6187d7f52f1ad571fd70ebe5ff391da9f214";
const juce::String uiPin = "2643eace79c5fa2462494389ceb87864cc646dfe";

juce::String describe (const juce::String& path, const juce::String& commit)
{
    return "git -C " + path + " describe --tags --match v* --always " + commit;
}

// The umbrella of b4347ea as git answers for it: a3-core, a3-motion (with its ui) and a3-mixer checked
// out, the rest not.
void answerAsCheckedOut (FakeRunner& runner)
{
    runner.answer ("git -C " + repo + " describe --tags --match v* --always HEAD", 0, "v03.0-271-g96dcb0d");
    runner.answer ("git -C " + repo + " ls-tree HEAD", 0, fixture ("git-ls-tree.txt"));
    runner.answer (describe (repo + "/a3-core", corePin), 0, "v03.0-413-ga87fd28");
    runner.answer (describe (repo + "/a3-motion", motionPin), 0, "v03.0");
    runner.answer ("git -C " + repo + "/a3-motion ls-tree " + motionPin, 0,
                   "100644 blob 1111111111111111111111111111111111111111\tREADME.md\n"
                   "040000 tree 2222222222222222222222222222222222222222\tfirmware\n"
                   "160000 commit " + uiPin + "\tui");
    runner.answer (describe (repo + "/a3-motion/ui", uiPin), 0, "v03.0-855-g2643eac");
    runner.answer ("git -C " + repo + "/a3-motion log -1 --format=%H " + motionPin + " -- firmware", 0, "f06bd6af");
    runner.answer (describe (repo + "/a3-motion", "f06bd6af"), 0, "v03.0-80-gf06bd6a");
    runner.answer ("git -C " + repo + "/a3-motion rev-parse " + motionPin + ":firmware", 0, "3435ade1265a41b4d4d73581b9a3cee2ee4415be");
    runner.answer (describe (repo + "/a3-mixer", mixerPin), 0, "v03.0-147-g16f805a");
    runner.answer ("git -C " + repo + "/a3-mixer log -1 --format=%H " + mixerPin + " -- hardware/mainboard/firmware", 0, "d331b69");
    runner.answer (describe (repo + "/a3-mixer", "d331b69"), 0, "v03.0-150-gd331b69");
    // Not checked out: git says so on stderr, which the runner hands on with the output.
    runner.answer (describe (repo + "/stemdeck", "1f177542ac768862d9ab287c17a640bf87d1f976"), 128,
                   "fatal: not a git repository (or any of the parent directories): .git");
}

juce::String tagOf (const SystemFacts& system, const juce::String& name)
{
    for (const auto& row : system.rows)
        if (row.name == name)
            return row.tag;
    ADD_FAILURE() << "no row " << name;
    return {};
}
}

TEST (System, ARevisionIsItsReleaseTagAndTheCommitsSince)
{
    EXPECT_EQ (releaseText ("v03.0"), "v03.0") << "on the tag";
    EXPECT_EQ (releaseText ("v03.0-413-ga87fd28"), "v03.0+413");
    EXPECT_EQ (releaseText ("a3-engine-v03.0-2-gabc1234"), "a3-engine-v03.0+2") << "a tag with dashes in it";
    EXPECT_EQ (releaseText ("a87fd28"), "a87fd28") << "no release tag before it: the commit";
    EXPECT_EQ (releaseText (""), "");
}

TEST (System, TheUmbrellaRecordsItsSubmodulesAsGitlinks)
{
    const auto links = parseGitlinks (fixture ("git-ls-tree.txt"));
    juce::StringArray paths;
    for (const auto& link : links)
        paths.add (link.path);
    EXPECT_EQ (paths.joinIntoString (" "), "a3-core a3-doc a3-mixer a3-motion beat-analyzer stemdeck stemseparator");
    EXPECT_EQ (links[3].commit, motionPin);
}

TEST (System, EachSubmoduleWithTheTagOfItsPinnedCommit)
{
    FakeRunner runner;
    answerAsCheckedOut (runner);
    const auto system = readSystem (runner, juce::File (repo));
    EXPECT_TRUE (system.found);
    EXPECT_EQ (system.version, "v03.0+271");
    juce::StringArray names;
    for (const auto& row : system.rows)
        names.add (row.name);
    EXPECT_EQ (names.joinIntoString (", "), "a3-core, a3-doc, a3-mixer, a3-mixer firmware, a3-motion, a3-motion firmware, "
                                             "a3-motion/ui, beat-analyzer, stemdeck, stemseparator");
    EXPECT_EQ (tagOf (system, "a3-core"), "v03.0+413");
    EXPECT_EQ (tagOf (system, "a3-motion"), "v03.0");
    EXPECT_EQ (tagOf (system, "a3-motion/ui"), "v03.0+855") << "a3-motion's own submodule";
}

// The firmware is the tag of the last commit that changed it, at the pin.
TEST (System, TheFirmwareIsTheTagOfItsLastChange)
{
    FakeRunner runner;
    answerAsCheckedOut (runner);
    const auto system = readSystem (runner, juce::File (repo));
    EXPECT_EQ (tagOf (system, "a3-motion firmware"), "v03.0+80");
    EXPECT_EQ (tagOf (system, "a3-mixer firmware"), "v03.0+150");
    EXPECT_EQ (system.motionFirmwareTree, "3435ade1265a41b4d4d73581b9a3cee2ee4415be");
    EXPECT_EQ (system.motionFirmwareTag, "v03.0+80");
}

TEST (System, ASubmoduleNotCheckedOutHasNoTag)
{
    FakeRunner runner;
    answerAsCheckedOut (runner);
    const auto system = readSystem (runner, juce::File (repo));
    EXPECT_EQ (tagOf (system, "stemdeck"), "") << "git's complaint is no tag";
    EXPECT_EQ (tagOf (system, "a3-doc"), "");
    EXPECT_EQ (systemTagText (SystemRow { "stemdeck", {} }), "not checked out");
    EXPECT_EQ (systemTagText (SystemRow { "a3-core", "v03.0+413" }), "v03.0+413");
}

TEST (System, NoCheckoutIsNoSystem)
{
    FakeRunner runner;
    runner.answer ("git -C " + repo + " ls-tree HEAD", 128, "fatal: cannot change to '" + repo + "': No such file or directory");
    const auto system = readSystem (runner, juce::File (repo));
    EXPECT_FALSE (system.found);
    EXPECT_TRUE (system.rows.empty());
}

// What the installer last flashed onto the Motion panel (installer/roles/motion.py).
TEST (System, TheFlashedMotionFirmwareFromTheInstallState)
{
    EXPECT_EQ (flashedMotionFirmware (fixture ("install-state.txt")), "3435ade1265a41b4d4d73581b9a3cee2ee4415be");
    EXPECT_EQ (flashedMotionFirmware ("[motion]\nflash_firmware = ask\n"), "");
    EXPECT_EQ (flashedMotionFirmware (""), "");
}
