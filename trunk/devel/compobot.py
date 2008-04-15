
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

import sys, os

import prefs
prefs = prefs.Preferences().data

class PluginList(object):
    def __init__(self):
        self.list = []
        self.descriptors = []

    def add_item(self, item, priority):
        self.descriptors.append([item, priority])
        self.build_list()

    def remove_item(self, item):
        for i in self.descriptors:
            if i[0].name == item:
                self.descriptors.remove(i)
        self.build_list()

    def reprioritize(self, item, priority):
        for i in xrange(len(self.descriptors)):
            if self.descriptors[i][0].name == item:
                self.descriptors[i][1] = priority
        self.build_list()

    def build_list(self):
        def sort_func(x, y):
            if x[1] > y[1]:
                return -1
            elif x[1] == y[1]:
                return 0
            return 1
        self.descriptors.sort(sort_func)
        new = []
        for i in self.descriptors:
            new.append(i[0])
        self.list = new

    def dispatch_event(self, command, args, do_all):
        for i in self.list:
            try:
                a = getattr(i, command)(*args)
                if a == True and not do_all:
                    break
            except:
                print "Error calling %s in plugin: %s with args: %s"%(command, i, args)

class SimpleBot(irc.IRCClient):
    nickname = prefs["nick"]
    password = prefs["password"]
    channel = '#' + prefs["channel"]

    def __init__(self):
        self.prefs = prefs

        self.plugin_list = PluginList()
        self.plugins = self.plugin_list.list

        self.loops = 0

        for i in prefs['plugins']:
            self.register_plugin(i)

    def register_plugin(self, plug):
        if type(plug) is type([]):
            plug, priority = plug
        else:
            priority = len(self.plugins)
        orig = plug
        if type(plug) is type(""):
            plug = get_plugin(plug)
        if plug:
            plug = plug(self, prefs)
            self.plugin_list.add_item(plug, priority)
            self.plugins = self.plugin_list.list
        else:
            print "plugin '%s' could not be loaded\nContinuing merrily..."%orig

    def remove_plugin(self, plug):
        self.plugin_list.remove_item(plug)
        self.plugins = self.plugin_list.list

    def reprioritize(self, plug, priority):
        self.plugin_list.reprioritize(plug, priority)
        self.plugins = self.plugin_list.list

    def send_to_plugins(self, command, args, do_all=False):
        self.plugin_list.dispatch_event(command, args, do_all)

    def connectionMade(self):
        """Called when we connect to the server."""
        irc.IRCClient.connectionMade(self)
        self.send_to_plugins("connect", ())

    def connectionLost(self, *other):
        """Called if we lose the connection."""
        irc.IRCClient.connectionLost(self)
        self.send_to_plugins("disconnect", ())

    def signedOn(self):
        """Called when bot has successfully signed on to server."""
        self.join(self.factory.channel)
        self.send_to_plugins("signon", ())

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.send_to_plugins("join", (channel,))

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        self.send_to_plugins("anymessage", (user, channel, msg))

        if self.nickname in msg:
            self.send_to_plugins("nickmessage", (user, channel, msg))

        elif channel == self.nickname:
            self.send_to_plugins("privatemessage", (user, channel, msg))

        else:
            #regular msg?
            self.send_to_plugins("generalmessage", (user, channel, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split("!", 1)[0]
        self.send_to_plugins("action", (user, channel, msg))

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split("!")[0]
        new_nick = params[0]
        self.send_to_plugins("usernickchange", (old_nick, new_nick))

    def make_reactor_call(self, *blank):
        self.send_to_plugins("reactorchance", (reactor,), True)
        reactor.callLater(0, self.make_reactor_call, ())

    def __kill_reactor(self, *blank):
        self.send_to_plugins("disconnect", ())
        reactor.stop()

    def stop_serving(self):
        reactor.callLater(0.5, self.__kill_reactor, ())


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
        
