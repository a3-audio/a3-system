from .core import Core
from .mixer import Mixer
from .motion import Motion
from .stemdeck import StemDeck

# The order they are installed in: the Core first, since StemDeck and Motion
# UI on the same machine run against its JACK.
ALL = (Core(), StemDeck(), Motion(), Mixer())
BY_NAME = {role.name: role for role in ALL}
