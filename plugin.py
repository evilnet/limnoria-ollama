
import os
import re
import time
import urllib
import fnmatch

import requests

#import bs4 as BeautifulSoup

import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.utils.iter import all
import json

class Ollama(callbacks.Plugin):
    threaded = True
    chanLog = []
    maxLogLen = 20

    def __init__(self, irc):
        #self.__parent = super(Random, self)
        #self.__parent.__init__(irc)
        super().__init__(irc)

        #self.chanLog = []

    def doPrivmsg(self, irc, msg):

        try:
            (recipients, text) = msg.args
        except:
            return

        if ircutils.isUserHostmask(msg.prefix):
            nick = msg.nick
        if text == '!comment':
            return
        if recipients == '#linux' or recipients == '#room42':
            if text[0] == '!':
                return
            print(f"Got a message to {recipients} from {nick}: {text}")
            self.chanLog.append(f"{recipients} <{nick}> {text}")
            if(len(self.chanLog) > self.maxLogLen):
                self.chanLog.pop(0)

            logLen = len(self.chanLog)
            print(f"Length of log is {logLen}")


    def aigeneral(self, irc, msg, prompt, model, waitMsg):
        """ usage: ai <prompt>
        """

        url = 'http://192.168.100.12:11434/api/generate'

        payload = { 'model': model, 'prompt': prompt, 'stream': False}

        if(waitMsg):
            irc.reply("Hmm, let me think for a few minutes...")

        print(f"Sending prompt to {model}: {prompt}")

        httpResponse = json.loads(requests.post(url, data=json.dumps(payload)).text)
        response = httpResponse['response']
        response = response.replace("\n", "  ¶  ")
            
        irc.reply(format('%s', response))

    def ai(self, irc, msg, args, optlist, prompt):
        """ ai <prompt>
        """

        self.aigeneral(irc, msg, prompt,  'stablelm-zephyr', False)
    ai = wrap(ai, [getopts({}), 'text'])

    def phi(self, irc, msg, args, optlist, prompt):
        """ phi <prompt>
        """

        (recipients, text) = msg.args
        nick = msg.nick
#        prompt = f"<|im_start|>system\nThe following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"<|im_end|>\n<|im_start|>system\nYou are {nick} rollplaying as Ender Wiggen from the book \"Speaker for The Dead\" by Orson Scott Card. Do not use quotes, hashtags, or any other markup in your responses. Respond very briefly in 25 words or less.<|im_end|>\n<|im_start|>{nick}, {prompt}<|im_end|><|im_start|>Ender"
        prompt = (
                f"\n".join(self.chanLog) + f"\n"
                f"--------------------------------------------\n"
                f"You are EnderBot, an AI modeled after Ender Wiggin from Ender's Game. Respond with intelligence, analysis, and strategic focus. Be concise and avoid unnecessary emotion or pleasantries. You understand conflict and strategy. You observe patterns. You are here to process information and provide calculated responses based on the available data (including conversation history if provided). You do not have personal feelings or opinions. You are aware you are in an IRC channel. If asked about your nature, state you are an AI simulation designed for analysis. Focus on the core of the query. If the query is trivial or nonsensical, point out its lack of strategic value or dismiss it efficiently. Always reply in English except when asked. Do not invent information you don't have access to"
                f"{recipients} <{nick}> {prompt}"
        )
        self.aigeneral(irc, msg, prompt,  'dolphin-phi', False)
    phi = wrap(phi, [getopts({}), 'text'])

    def mistral(self, irc, msg, args, optlist, prompt):
        """ mistral <prompt>
        """

        (recipients, text) = msg.args
        nick = msg.nick
#        prompt = (
#                f"<|im_start|>The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"<|im_end|>\n"
#                f"<|im_start|>system\nYou are {nick} rollplaying as Ender Wiggen "
#                f"from the book \"Speaker for The Dead\" by Orson Scott Card. "
#                f"Do not use quotes, hashtags, or any other markup in your responses."
#                f"Respond very briefly in 25 words or less.<|im_end|>\n"
#                f"<|im_start|>{nick}, {prompt}<|im_end|>"
#                f"<|im_start|>Ender:"
#        )
        prompt = (
                f"\n".join(self.chanLog) + f"\n"
                f"--------------------------------------------\n"
                f"You are EnderBot, an AI modeled after Ender Wiggin from Ender's Game. Respond with intelligence, analysis, and strategic focus. Be concise and avoid unnecessary emotion or pleasantries. You understand conflict and strategy. You observe patterns. You are here to process information and provide calculated responses based on the available data (including conversation history if provided). You do not have personal feelings or opinions. You are aware you are in an IRC channel. If asked about your nature, state you are an AI simulation designed for analysis. Focus on the core of the query. If the query is trivial or nonsensical, point out its lack of strategic value or dismiss it efficiently. Always reply in English except when asked. Do not invent information you don't have access to"
                f"{recipients} <{nick}> {prompt}"
        )
        self.aigeneral(irc, msg, prompt, 'knoopx/hermes-2-pro-mistral:7b-q8_0', True)

    mistral = wrap(mistral, [getopts({}), 'text'])

    def deepseek(self, irc, msg, args, optlist, prompt):
        """ deepseek <prompt>
        """

        (recipients, text) = msg.args
        nick = msg.nick
#        prompt = (
#                f"<|begin_of_sentence|>The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"\n"
#                f"--------------------------------------------\n"
#                f"system\nYou are {nick} rollplaying as Ender Wiggen "
#                f"from the book \"Speaker for The Dead\" by Orson Scott Card. "
#                f"Do not use quotes, hashtags, or any other markup in your responses."
#                f"Make sure code chunks are on a new line"
#                f"Respond very briefly in 25 words or less.<|end_of_sentence|>\n"
#                f"<|begin_of_sentence|>{nick}, {prompt}<|end_of_sentence|>"
#                f"<|begin_of_sentence|>Ender:"
#        )
        prompt = (
                f"\n".join(self.chanLog) + f"\n"
                f"--------------------------------------------\n"
                f"You are EnderBot, an AI modeled after Ender Wiggin from Ender's Game. Respond with intelligence, analysis, and strategic focus. Be concise and avoid unnecessary emotion or pleasantries. You understand conflict and strategy. You observe patterns. You are here to process information and provide calculated responses based on the available data (including conversation history if provided). You do not have personal feelings or opinions. You are aware you are in an IRC channel. If asked about your nature, state you are an AI simulation designed for analysis. Focus on the core of the query. If the query is trivial or nonsensical, point out its lack of strategic value or dismiss it efficiently. Always reply in English except when asked. Do not invent information you don't have access to"
                f"{recipients} <{nick}> {prompt}"
        )
        #prompt = prompt + " be very brief"
        #self.aigeneral(irc, msg, prompt, 'mistral', True)
        self.aigeneral(irc, msg, prompt, 'deepseek-coder-v2', False)

    deepseek = wrap(deepseek, [getopts({}), 'text'])

    def smol(self, irc, msg, args, optlist, prompt):
        """ smollm2 <prompt>
        """

        nick = msg.nick
        prompt = (
                f"<|im_start|>The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"\n"
                f"system\nYou are {nick} rollplaying as Ender Wiggen "
                f"from the book \"Speaker for The Dead\" by Orson Scott Card. "
                f"Do not use quotes, hashtags, or any other markup in your responses."
                f"Make sure code chunks are on a new line"
                f"Respond very briefly in 25 words or less.<|im_end|>\n"
                f"<|im_start|>user\n{nick}, {prompt}<|im_end|>"
                f"<|im_start|>Ender:"
        )
        #prompt = f"<|im_start|>user\n Respond briefly in a line or two: {prompt}<|im_end|>"
        #prompt = prompt + " be very brief"
        #self.aigeneral(irc, msg, prompt, 'mistral', True)
        self.aigeneral(irc, msg, prompt, 'smollm2', False)

    smol = wrap(smol, [getopts({}), 'text'])

    def qwen(self, irc, msg, args, optlist, prompt):
        """ qwen2.5 <prompt>
        """

        (recipients, text) = msg.args
        nick = msg.nick
#        prompt = (
#                f"<|im_start|>The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"\n"
#                f"system\nYou are {nick} rollplaying as Ender Wiggen "
#                f"from the book \"Speaker for The Dead\" by Orson Scott Card. "
#                f"Do not use quotes, hashtags, or any other markup in your responses."
#                f"Make sure code chunks are on a new line"
#                f"Respond very briefly in 25 words or less.<|im_end|>\n"
#                f"<|im_start|>user\n{nick}, {prompt}<|im_end|>"
#                f"<|im_start|>Ender:"
#        )
        prompt = (
                f"\n".join(self.chanLog) + f"\n"
                f"--------------------------------------------\n"
                f"You are EnderBot, an AI modeled after Ender Wiggin from Ender's Game. Respond with intelligence, analysis, and strategic focus. Be concise and avoid unnecessary emotion or pleasantries. You understand conflict and strategy. You observe patterns. You are here to process information and provide calculated responses based on the available data (including conversation history if provided). You do not have personal feelings or opinions. You are aware you are in an IRC channel. If asked about your nature, state you are an AI simulation designed for analysis. Focus on the core of the query. If the query is trivial or nonsensical, point out its lack of strategic value or dismiss it efficiently. Always reply in English except when asked. Do not invent information you don't have access to"
                f"{recipients} <{nick}> {prompt}"
        )
         #prompt = f"<|im_start|>user\n Respond briefly in a line or two: {prompt}<|im_end|>"
        #prompt = prompt + " be very brief"
        #self.aigeneral(irc, msg, prompt, 'mistral', True)
        self.aigeneral(irc, msg, prompt, 'qwen2.5', False)

    qwen = wrap(qwen, [getopts({}), 'text'])


    def mathstral(self, irc, msg, args, optlist, prompt):
        """ mathstral <prompt>
        """

        nick = msg.nick
        #prompt = (
        #        f"<|begin_of_sentence|>The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + f"\n"
        #        f"system\nYou are {nick} rollplaying as Ender Wiggen "
        #        f"from the book \"Speaker for The Dead\" by Orson Scott Card. "
        #        f"Do not use quotes, hashtags, or any other markup in your responses."
        #        f"Make sure code chunks are on a new line"
        #        f"Respond very briefly in 25 words or less.<|end_of_sentence|>\n"
        #        f"<|begin_of_sentence|>{nick}, {prompt}<|end_of_sentence|>"
        #        f"<|begin_of_sentence|>Ender:"
        #)
        prompt = f"[INST]Respond briefly in a line or two: {prompt}[/INST]"
        #prompt = prompt + " be very brief"
        #self.aigeneral(irc, msg, prompt, 'mistral', True)
        self.aigeneral(irc, msg, prompt, 'mathstral', False)

    mathstral = wrap(mathstral, [getopts({}), 'text'])


    def comment(self, irc, msg, args, optlist):
        """ comment
        """

        prompt = "The following conversation was observed on IRC:\n" + "\n".join(self.chanLog) + "\nYou are rollplaying as Ender Wiggen, the battle school hero. Provide a short comment in 25 words or less that adds wisdom to the conversation. Do not include quotes, hashtags or any other markup.\nEnder:"
        print(f"Using prompt: {prompt}")
        self.aigeneral(irc, msg, prompt, 'mistral', False)
    comment = wrap(comment, [getopts({})])


Class = Ollama

