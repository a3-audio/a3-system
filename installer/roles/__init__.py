from .core import Core
from .deckhost import DeckHost
from .desk import Desk
from .mixer import Mixer
from .motion import Motion
from .stemdeck import StemDeck

# The order they are installed in: the Core first, since StemDeck and Motion
# UI on the same machine run against its JACK. deck-host before Motion: it
# writes Motion's panel drop-in, which Motion's restart then reads.
ALL = (Core(), StemDeck(), DeckHost(), Motion(), Desk(), Mixer())
BY_NAME = {role.name: role for role in ALL}


def needed_submodules(names, from_source):
    """The submodules the named roles need, in install order, once each: what
    they read configuration from, plus what builds when built from source."""
    paths = []
    for role in ALL:
        if role.name not in names:
            continue
        wanted = role.config_submodules + (role.submodules if from_source else ())
        paths.extend(p for p in wanted if p not in paths)
    return paths


def needed_packages(names, from_source):
    """The Debian packages the named roles need, sorted, once each: what runs,
    plus what builds when the apps are built from source."""
    roles = [role for role in ALL if role.name in names]
    needed = {p for role in roles for p in role.packages}
    if from_source:
        needed |= {p for role in roles for p in role.build_packages}
    return sorted(needed)


def needs_screen(names):
    """Whether any of the named roles draws on this machine's screen."""
    return any(role.needs_screen for role in ALL if role.name in names)
