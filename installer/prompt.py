"""Asking the person at the machine: whiptail menus, plain text, or nobody.

whiptail is the Debian installer's dialog program and is on every Debian and
Raspberry Pi OS; without it, or without a terminal, questions are plain text.
Windows and macOS (from the first release on) take the text path too.
A non-interactive prompter answers every question with its default -- which
is the stored answer -- so `install --config` and `--update` ask nothing.
"""

import shutil
import subprocess
import sys

TITLE = "A³ System"


class Prompter:
    """Answers with the defaults. The base for the two that ask."""

    interactive = False

    def yesno(self, question, default):
        return default

    def text(self, question, default):
        return default

    def choose(self, question, options, default):
        """One of `options`, a list of (key, label)."""
        return default

    def checklist(self, question, options, chosen):
        """Several of `options`, a list of (key, label); `chosen` are ticked."""
        return list(chosen)

    def note(self, message):
        print(message)


class TextPrompter(Prompter):
    interactive = True

    def __init__(self, read=input, write=print):
        self._read = read
        self._write = write

    def yesno(self, question, default):
        hint = "J/n" if default else "j/N"
        while True:
            answer = self._read(f"{question} [{hint}] ").strip().lower()
            if not answer:
                return default
            if answer in ("j", "ja", "y", "yes"):
                return True
            if answer in ("n", "nein", "no"):
                return False

    def text(self, question, default):
        answer = self._read(f"{question} [{default}] ").strip()
        return answer or default

    def choose(self, question, options, default):
        self._write(question)
        for number, (key, label) in enumerate(options, 1):
            mark = "*" if key == default else " "
            self._write(f"  {mark}{number}) {label}")
        while True:
            answer = self._read("Nummer (Enter = *): ").strip()
            if not answer:
                return default
            if answer.isdigit() and 1 <= int(answer) <= len(options):
                return options[int(answer) - 1][0]

    def checklist(self, question, options, chosen):
        self._write(question)
        for number, (key, label) in enumerate(options, 1):
            mark = "x" if key in chosen else " "
            self._write(f"  [{mark}] {number}) {label}")
        while True:
            answer = self._read("Nummern mit Leerzeichen, - für keine (Enter = [x]): ").strip()
            if not answer:
                return list(chosen)
            if answer == "-":
                return []
            numbers = answer.replace(",", " ").split()
            if all(n.isdigit() and 1 <= int(n) <= len(options) for n in numbers):
                picked = {options[int(n) - 1][0] for n in numbers}
                return [key for key, _ in options if key in picked]

    def note(self, message):
        self._write(message)


class WhiptailPrompter(Prompter):
    """whiptail draws on the terminal and writes the answer to stderr."""

    interactive = True

    def _run(self, args):
        done = subprocess.run(["whiptail", "--title", TITLE, *args],
                              stderr=subprocess.PIPE, text=True)
        return done.returncode, done.stderr.strip()

    @staticmethod
    def _height(lines):
        return str(min(24, 8 + lines))

    def yesno(self, question, default):
        args = ["--yesno", question, "12", "72"]
        if not default:
            args.insert(0, "--defaultno")
        code, _ = self._run(args)
        if code == 255:
            raise KeyboardInterrupt
        return code == 0

    def text(self, question, default):
        code, answer = self._run(["--inputbox", question, "10", "72", default])
        if code != 0:
            raise KeyboardInterrupt
        return answer

    def choose(self, question, options, default):
        items = []
        for key, label in options:
            items += [key, label, "ON" if key == default else "OFF"]
        code, answer = self._run(["--radiolist", question,
                                  self._height(len(options)), "72",
                                  str(len(options)), *items])
        if code != 0:
            raise KeyboardInterrupt
        return answer or default

    def checklist(self, question, options, chosen):
        items = []
        for key, label in options:
            items += [key, label, "ON" if key in chosen else "OFF"]
        code, answer = self._run(["--separate-output", "--checklist", question,
                                  self._height(len(options)), "72",
                                  str(len(options)), *items])
        if code != 0:
            raise KeyboardInterrupt
        picked = set(answer.split())
        return [key for key, _ in options if key in picked]

    def note(self, message):
        print(message)


def make_prompter(interactive):
    if not interactive:
        return Prompter()
    if sys.stdin.isatty() and shutil.which("whiptail"):
        return WhiptailPrompter()
    return TextPrompter()
