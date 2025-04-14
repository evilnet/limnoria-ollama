import supybot.conf as conf
import supybot.registry as registry

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('AttackProtector')
except:
    _ = lambda x:x

def configure(advanced):
    from supybot.questions import output, expect, anything, something, yn
    conf.registerPlugin('Ollama', True)


Ollama = conf.registerPlugin("Ollama")
conf.registerChannelValue(Ollama, 'bold', registry.Boolean(True, _("""Determine wether the plugin will use bold in the responses.""")))

conf.registerGroup(Ollama, 'defaults')
conf.registerChannelValue(Ollama.defaults, 'model', registry.String('any', _("""Determines the default language model to use""")))


