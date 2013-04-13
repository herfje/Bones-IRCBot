# -*- encoding: utf8 -*-
import re
import sys

from twisted.words.protocols import irc
from twisted.internet import protocol


reCommand = re.compile("\.([a-zA-Z0-9]*)( .+)*?")


class BonesBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def _get_versionName(self):
        return self.factory.versionName
    versionName = property(_get_versionName)
    
    def _get_versionNum(self):
        return self.factory.versionNum
    versionNum = property(_get_versionNum)
    
    def _get_versionEnv(self):
        return self.factory.versionEnv
    versionEnv = property(_get_versionEnv)
    
    def _get_sourceURL(self):
        return self.factory.sourceURL
    sourceURL = property(_get_sourceURL)
    
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
        print "Signed on as %s." % (self.nickname,)
    
    def joined(self, channel):
        print "Joined %s." % (channel,)
    
    def privmsg(self, user, channel, msg):
        data = reCommand.match(msg)
        if data:
            trigger = data.group(1)
            print "Received trigger %s." % (trigger,)
            for module in self.factory.modules:
                if trigger in module.triggerMap and callable(module.triggerMap[trigger]):
                    module.triggerMap[trigger](module, self, user=user, channel=channel, args=data, msg=msg)


class BonesBotFactory(protocol.ClientFactory):
    versionName = "Bones-IRCBot"
    versionNum = "0.0"
    versionEnv = sys.platform
    sourceURL = "https://github.com/404d/Bones-IRCBot"

    protocol = BonesBot
    modules = []
    
    def __init__(self, settings, nickname="Bones"):
        self.channels = settings.get("bot", "channel").split("\n")
        self.nickname = settings.get("bot", "nickname")
    
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

class Module():
    triggerMap = {}
