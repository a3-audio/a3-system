"""The screen every screen role draws on: the user logged in on tty1, X
started by startx, i3 on it. No display manager.

Standard Debian: getty logs the user in on tty1 (a drop-in for
getty@tty1.service), ~/.bash_profile starts X there, ~/.xinitrc starts i3.
lightdm is disabled, not purged. Run once by the installer before the
roles, when any chosen role needs a screen; the same steps on every run.
"""

import shutil
from pathlib import Path

AUTOLOGIN_UNIT = "getty@tty1.service"
AUTOLOGIN_DROP_IN = Path("/etc/systemd/system") / f"{AUTOLOGIN_UNIT}.d" / "a3-autologin.conf"

BLOCK_BEGIN = "# >>> a3-system autologin >>>"
BLOCK_END = "# <<< a3-system autologin <<<"

XINITRC_MARKER = "# a3-system autologin: written by the installer, rewritten on every run."
# a3-core's a3-reaper and qjackctl units set no DISPLAY: they get it from the
# systemd user manager. Under lightdm, Xsession.d imported it; with startx
# nothing does unless ~/.xinitrc says so. The explicit import does not depend
# on the dbus tools; Xsession afterwards runs the rest of what lightdm ran
# (Xresources, the dbus environment, unclutter) and starts i3.
XINITRC_TEXT = f"""{XINITRC_MARKER}
systemctl --user import-environment DISPLAY XAUTHORITY
if [ -x /etc/X11/Xsession ]; then
    exec /etc/X11/Xsession i3
fi
exec i3
"""

# What has to be there for the next boot to come up in X, not on a console.
SCREEN_PROGRAMS = ("startx", "Xorg", "i3")


def autologin_drop_in(user):
    # The empty ExecStart= resets the unit's own before replacing it.
    return ("[Service]\n"
            "ExecStart=\n"
            f"ExecStart=-/sbin/agetty --autologin {user} --noclear %I $TERM\n")


def autologin_block():
    return (f"{BLOCK_BEGIN}\n"
            "# X on tty1 only, and only once: not over ssh, not inside X.\n"
            'if [ -z "$DISPLAY" ] && [ "$(tty)" = /dev/tty1 ]; then\n'
            "    exec startx\n"
            "fi\n"
            f"{BLOCK_END}\n")


def _new_bash_profile():
    # bash reads ~/.bash_profile instead of ~/.profile, so a new one has to
    # read ~/.profile itself, or PATH and the rest go missing.
    return "[ -f ~/.profile ] && . ~/.profile\n\n" + autologin_block()


def with_autologin_block(text):
    """~/.bash_profile with the installer's block: the file's text, or None
    when there is none. A present block is replaced, a foreign file gets it
    appended; nothing else in it changes."""
    if text is None:
        return _new_bash_profile()
    begin = text.find(BLOCK_BEGIN + "\n")
    end = text.find(BLOCK_END + "\n", begin)
    if begin >= 0 and end >= 0:
        return text[:begin] + autologin_block() + text[end + len(BLOCK_END) + 1:]
    if text and not text.endswith("\n"):
        text += "\n"
    return text + ("\n" if text else "") + autologin_block()


def _write_home_file(ctx, path, text):
    ctx.runner.log(f"# {path}:\n" + "".join(f"#   {line}\n" for line in text.splitlines()))
    if not ctx.runner.dry_run:
        path.write_text(text)


def ensure_bash_profile(ctx):
    path = ctx.home / ".bash_profile"
    current = path.read_text() if path.exists() else None
    wanted = with_autologin_block(current)
    if wanted != current:
        _write_home_file(ctx, path, wanted)


def ensure_xinitrc(ctx):
    path = ctx.home / ".xinitrc"
    if path.exists() and XINITRC_MARKER not in path.read_text():
        ctx.runner.log(f"{path} ist von Hand geschrieben und wird gelassen, wie sie ist. "
                       "Sie muss i3 starten und DISPLAY/XAUTHORITY an systemd --user "
                       "geben, sonst finden REAPER und qjackctl kein X.")
        return
    _write_home_file(ctx, path, XINITRC_TEXT)


def write_autologin_drop_in(ctx):
    ctx.runner.run(["install", "-D", "-m", "644", "/dev/stdin", AUTOLOGIN_DROP_IN],
                   root=True, input=autologin_drop_in(ctx.user))


def disable_lightdm(ctx):
    # check=False: a machine without lightdm is the goal, not an error.
    ctx.runner.run(["systemctl", "disable", "lightdm"], root=True, check=False)
    ctx.runner.run(["systemctl", "daemon-reload"], root=True)


def screen_problems(home, which=shutil.which):
    """What would leave the next boot on a console instead of in X."""
    problems = []
    profile = Path(home) / ".bash_profile"
    if not profile.exists() or autologin_block() not in profile.read_text():
        problems.append(f"{profile} startet X nicht (der a3-system-Block fehlt)")
    problems.extend(f"{program} fehlt" for program in SCREEN_PROGRAMS if not which(program))
    return problems


def _verify_drop_in(ctx):
    if not shutil.which("systemd-analyze"):
        ctx.runner.log("systemd-analyze fehlt, der Autologin-Drop-in bleibt ungeprüft.")
        return []
    # --man=no: without man the check failed on the unit's own man pages, not on
    # the drop-in (a3-system#77).
    code = ctx.runner.run(["systemd-analyze", "verify", "--man=no", AUTOLOGIN_UNIT],
                          check=False)
    if code != 0:
        return [f"systemd-analyze verify {AUTOLOGIN_UNIT} meldet Fehler (siehe oben)"]
    return []


def set_up_screen(ctx):
    """Autologin on tty1 into X with i3, for the next boot. Returns the
    problems found afterwards; empty when the machine will come up in X."""
    run = ctx.runner
    write_autologin_drop_in(ctx)
    ensure_bash_profile(ctx)
    ensure_xinitrc(ctx)
    disable_lightdm(ctx)
    problems = _verify_drop_in(ctx)
    if not run.dry_run:
        problems += screen_problems(ctx.home)
    run.log(f"{ctx.user} wird ab dem nächsten Neustart auf tty1 angemeldet und startet "
            "X mit i3, ohne lightdm. lightdm ist nur abgeschaltet; entfernen mit "
            "sudo apt purge lightdm")
    return problems
