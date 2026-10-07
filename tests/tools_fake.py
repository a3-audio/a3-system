"""A stand-in for the tools' runner and for the person at the keyboard.

Nothing here runs a command: a test scripts the replies, and reads back
what the tool would have run.
"""

import importlib.machinery
import importlib.util
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))


def load_tool(name):
    """Import an executable tool that has no .py suffix."""
    loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(TOOLS / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class FakeRunner:
    """Replies are (prefix, returncode, stdout, stderr); the first reply whose
    prefix starts the command answers it. Unscripted commands succeed silently."""

    def __init__(self, replies=()):
        self.replies = list(replies)
        self.calls = []

    def _reply(self, args):
        for prefix, code, out, err in self.replies:
            if list(args[:len(prefix)]) == list(prefix):
                return code, out, err
        return 0, "", ""

    def capture(self, args):
        self.calls.append(("capture", list(args)))
        code, out, err = self._reply(args)
        return subprocess.CompletedProcess(list(args), code, out, err)

    def run(self, args):
        self.calls.append(("run", list(args)))
        return self._reply(args)[0]

    def ran(self):
        """The commands that change something."""
        return [args for kind, args in self.calls if kind == "run"]

    def everything(self):
        return [args for _, args in self.calls]


class Answers:
    """Answers questions in order; asking past the end is a test failure."""

    def __init__(self, *answers):
        self.answers = list(answers)
        self.questions = []

    def __call__(self, question):
        self.questions.append(question)
        if not self.answers:
            raise AssertionError(f"unexpected question: {question}")
        answer = self.answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer


class Output(list):
    def __call__(self, line=""):
        self.append(str(line))

    def text(self):
        return "\n".join(self)
