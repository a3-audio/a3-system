from .core import Core
from .mixer import Mixer
from .motion import Motion
from .stemdeck import StemDeck

# The order they are installed in: the Core first, since StemDeck and Motion
# UI on the same machine run against its JACK.
ALL = (Core(), StemDeck(), Motion(), Mixer())
BY_NAME = {role.name: role for role in ALL}


def needed_submodules(names):
    """The submodules the named roles build from, in install order, once each."""
    paths = []
    for role in ALL:
        if role.name not in names:
            continue
        paths.extend(p for p in role.submodules if p not in paths)
    return paths


def needed_packages(names):
    """The Debian packages the named roles build against, sorted, once each."""
    return sorted({p for role in ALL if role.name in names for p in role.packages})
