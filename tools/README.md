# Maintainer tools

Small command-line helpers for the A³ build and deploy path. Python 3, standard library only.
Run them from this directory or put it on `PATH`.

| Command | Runs on | What it does |
|---|---|---|
| `a3-update [--yes] [--dry-run] [package …]` | the rig machines (a3nuc1, a3nuc2) | `sudo apt update`, then shows installed → candidate for every package of the A³ apt source (`http://192.168.8.5/apt a3 main`) or the named ones, asks once, installs only those with `apt-get install --allow-change-held-packages` and holds them again. Asks per package before restarting its user service (`a3-motion-ui`: `a3-motion.service`; default No). Never `apt upgrade`, never `apt autoremove`. `--yes` skips the update question, not the restart one; `--dry-run` only prints the plan. |
| `a3-build-status` | a3coreV01 | The build queue, the state of `a3-build.service` (with the last run's result when idle) and `a3-build.path`, the published versions, and the last 10 `a3-build:` lines of the build log plus systemd's last result line — no compiler output. Needs no rights; what the user may not read (queue, journal) is said instead. Reading the log needs group `adm`. |
| `a3-rebuild <repo> [commit]` | a3coreV01 | Queues a build by hand, the way the gitolite hook does. The commit defaults to the repo's `main` on the local gitolite; writing the queue entry runs `sudo -u git`. Follow it with `a3-build-status` or `sudo journalctl -u a3-build -f`. |

Tests: `python3 -m unittest discover -s tests` from the repository root (`tests/test_tools_*.py`);
they never run apt, sudo, systemctl, journalctl or git.
