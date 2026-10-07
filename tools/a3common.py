"""What the maintainer tools share: one way to run commands, one way to ask.

Every command a tool runs goes through Runner, so the tests can swap it for
a fake and never touch apt, sudo, systemctl, journalctl or git.
"""

import subprocess


class Runner:
    def capture(self, args):
        """Run a command that only looks; its output comes back, it never raises."""
        try:
            return subprocess.run(list(args), capture_output=True, text=True)
        except FileNotFoundError:
            return subprocess.CompletedProcess(list(args), 127, "", f"{args[0]}: not found\n")

    def run(self, args):
        """Run a command that changes something, on the terminal (sudo may ask
        for a password). Returns the exit code."""
        try:
            return subprocess.run(list(args)).returncode
        except FileNotFoundError:
            return 127


def ask_yes(question, ask=input):
    """True only on an explicit yes: Enter, anything else, or no input is No."""
    try:
        answer = ask(question)
    except (EOFError, KeyboardInterrupt):
        return False
    return answer.strip().lower() in ("y", "yes")
