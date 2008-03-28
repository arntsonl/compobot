"""
    CompoBot.py

    @summary: An IRC bot for managing teams during coding competitions. Uses plugins to
    control functionality.

    @version: 0.1.1

    @author: RB[0]
    @author: Cthulhu32
    @author: Keeyai

    @note: Requires Twisted

    Events to add callbacks for and their parameters:
        Event                   Params                          Description
        connect                 None                            Called when bot connects to the server
        disconnect              reason                          Called when bot disconnects from the server
        signon                  None                            Called when bot signs on to the server
        join                    channel                         Called when bot joins a channel
        generalmessage          user, channel, message          Called when a user sends a message to a channel
        privatemessage          user, message                   Called when a user sends the bot a private message
        nickmessage             user, channel, message          Called when a user sends a message with the botname in it
        action                  user, channel, message          Called when a user does an !action in a channel
        usernickchange          oldnick, newnick                Called when a user changes their name from oldnick to newnick

        --------------
        log - NYI
        selfnickchange - NYI

    @todo: changelog, chat filtering, scheduling


    @change: 0.1.0 - Keeyai's plugins
    @change: 0.1.0 - Cthulhu's preference loaded

"""

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, os
import prefs

botPrefs = prefs.Preferences()
class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

        print message

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = botPrefs.data["nick"]

    # dictionary of events and their lists of callbacks
    eventCallbacks = {'connect':[], 'signon': [], 'join':[], 'generalmessage':[], 'privatemessage':[],
                    'nickmessage':[], 'action':[], 'reconnect':[], 'disconnect':[], 'log':[],
                    'usernickchange':[], 'selfnickchange':[]}

    def __init__(self):
        """Initializes the bot. Loads preferences and plugins."""

        self.channel = None

        # load plugins
        self.loadPlugins()


    def loadPlugins(self):
        """Loads all the plugins in the ./plugins folder."""


        # add our plugins folder to the path
    #    pluginpath = os.path.join(os.path.abspath('.'), "plugins")
    #    sys.path.insert(0, pluginpath)

        self.plugins = {}

        # test for plugins folder
        if os.path.exists('plugins'):

            # load each plugin
            for pluginname in os.listdir('plugins'):

                if not pluginname.startswith('.') and os.path.isdir( os.path.join('plugins', pluginname)):

                    print 'Loading Plugin: ', pluginname

                    # add folder to the path -- probably very obvious, easy way to skip this
                    sys.path.insert(0, os.path.join(os.path.abspath('.'), "plugins", pluginname))

                    # import the module
                    module = __import__(pluginname, None, None, 2)

                    # load and register the plugin
                    plugin = module.plugin()
                    plugin.register(self)

                    # save plugin
                    self.plugins[pluginname] = plugin

        # create plugins folder if necessary
        else:
            os.mkdir('plugins')

    def registerCallback(self, event, callback):
        # check that we are tracking this event
        if event in self.eventCallbacks.keys():
            self.eventCallbacks[event].append(callback)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

        for callback in self.eventCallbacks['connect']:
            try:
                callback()
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()

        for callback in self.eventCallbacks['disconnect']:
            try:
                callback(reason)
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

        for callback in self.eventCallbacks['signon']:
            try:
                callback()
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

        # save channel
        self.channel = channel

        for callback in self.eventCallbacks['join']:
            try:
                callback(channel)
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)


            for callback in self.eventCallbacks['privatemessage']:
                try:
                    callback(user, message)
                except Exception, e:
                    self.logger.log("Exception while calling %s: %s" % (callback, e))

            return

        # Otherwise check to see if it is a message directed at me
        if msg.find(self.nickname) != -1:
            self.logger.log("<%s> %s" % (self.nickname, msg))

            for callback in self.eventCallbacks['nickmessage']:
                try:
                    callback(user, channel, msg)
                except Exception, e:
                    self.logger.log("Exception while calling %s: %s" % (callback, e))

        # just a regular message
        else:
            for callback in self.eventCallbacks['generalmessage']:
                try:
                    callback(user, channel, msg)
                except Exception, e:
                    self.logger.log("Exception while calling %s: %s" % (callback, e))


    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

        for callback in self.eventCallbacks['action']:
            try:
                callback(user, channel, msg)
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


        for callback in self.eventCallbacks['usernickchange']:
            try:
                callback(old_nick, new_nick)
            except Exception, e:
                self.logger.log("Exception while calling %s: %s" % (callback, e))


class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.Protocol_stored = p
        return p

if __name__ == '__main__':
    def update_topic(f):
        y, m, d, h, min, e1, e2, e3, e4 = time.localtime(time.time())
        tday = 29
        thour = 19
        format = tday - d, thour - h, 60 - min
        toth = format[0] * 24 + format[1]
        if (toth > 2 and  min == 0 or\
           toth < 2 and 60 - min > 30 or\
           toth < 2 and 60 - min <= 30) and\
           e1 in range(30):
            f.Protocol_stored.topic("pyweek", """Pyweek | %s days, %s hours, %s minutes | theme voting: Robot, Shuffle, Mashed, Jig, Formation | some choices of gamelibs: | 2d: www.pygame.org | 3d: www.panda3d.org | 3d: http://pyopengl.sourceforge.net/ | 3d: http://home.gna.org/oomadness/en/soya3d/index.html | 2d-3d: http://www.pyglet.org/ | Web: http://www.djangoproject.com/"""%format)
        reactor.callLater(30, update_topic, f)

    # initialize logging
    log.startLogging(sys.stdout)

    sys.argv.append(botPrefs.data["channel"])
    sys.argv.append(botPrefs.data["logfile"])

    # create factory protocol and application
    f = LogBotFactory(sys.argv[1], sys.argv[2])

    # connect factory to this host and port
    reactor.connectTCP(botPrefs.data["server"], int(botPrefs.data["port"]), f)

    reactor.callLater(30, update_topic, f)

    # run bot
    reactor.run()
