"""
ollama stuff
"""

import supybot
import supybot.world as world

if 'reload' not in globals():
    from imp import reload

__version__ = "0.1"


__url__ = ""

from . import config
from . import plugin
from imp import reload

reload(plugin)

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure
