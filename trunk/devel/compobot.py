
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

import sys, os

import prefs
prefs = prefs.Preferences().data

class SimpleBot(irc.IRCClient):
    nickname = prefs["nick"]
    password = prefs["password"]
    channel = prefs["channel"]

    def __init__(self):
        self.prefs = prefs

        self.plugins = []

        self.loops = 0

        for i in prefs['plugins']:
            self.register_plugin(i)

    def register_plugin(self, plug):
        orig = plug
        if type(plug) is type(""):
            plug = get_plugin(plug)
        if plug:
            plug = plug(self, prefs)
            self.plugins.append(plug)
        else:
            print "plugin '%s' could not be loaded\nContinuing merrily..."%orig

    def send_to_plugins(self, command, args):
        for i in self.plugins:
            getattr(i, command)(*args)

    def connectionMade(self):
        """Called when we connect to the server."""
        irc.IRCClient.connectionMade(self)
        self.send_to_plugins("connect", ())

    def connectionLost(self, *other):
        """Called if we lose the connection."""
        irc.IRCClient.connectionLost(self)
        self.send_to_plugins("close", ())

    def signedOn(self):
        """Called when bot has successfully signed on to server."""
        self.join(self.factory.channel)
        self.send_to_plugins("signed_on", ())

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.send_to_plugins("join", (channel,))

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.msg(self.channel, "Test...")

        self.send_to_plugins("any_msg", (user, channel, msg))

        if self.nickname in msg:
            self.send_to_plugins("msg_with_name_in_it", (user, channel, msg))

        elif channel == self.nickname:
            self.send_to_plugins("priv_msg", (user, channel, msg))

        else:
            #regular msg?
            self.send_to_plugins("msg", (user, channel, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split("!", 1)[0]
        self.send_to_plugins("action", (user, channel, msg))

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split("!")[0]
        new_nick = params[0]
        self.send_to_plugins("change_nick", (old_nick, new_nick))

    def make_reactor_call(self, *blank):
        self.send_to_plugins("reactor_chance", (reactor,))
        reactor.callLater(0, self.make_reactor_call, ())

    def stop_serving(self):
        self.send_to_plugins("close", ())
        reactor.stop()


class SimpleBotFactory(protocol.ClientFactory):
    protocol = SimpleBot

    def __init__(self):
        self.channel = prefs["channel"]
        self.plugins = []

        self.buildProtocol(0)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self

        for i in self.plugins:
            p.register_plugin(i)
        self.bot = p
        return p

    def register_plugin(self, plug):
        self.plugins.append(plug)


def run_factory(factory):
    log.startLogging(sys.stdout)
    reactor.connectTCP(prefs["server"], prefs["port"], factory)
    reactor.callLater(0, factory.bot.make_reactor_call, ())

    reactor.run()

def get_plugin(name):
    try:
        try:
            if not "plugins" in sys.path:
                sys.path.append("plugins")
            a = __import__(name)
        except:
            pth = os.path.join(os.path.split(__file__)[0], "plugins")
            if not pth in sys.path:
                sys.path.append(pth)
            a = __import__(name)
        return a.Plugin
    except:
        pass


if __name__ == "__main__":
    f = SimpleBotFactory()

    run_factory(f)
        
