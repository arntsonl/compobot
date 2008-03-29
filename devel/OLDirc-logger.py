# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys


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

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = "RB[0]-bot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am a log bot" % user
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


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

    sys.argv.append("pyweek")
    sys.argv.append("pyweek_log1.txt")

    # create factory protocol and application
    f = LogBotFactory(sys.argv[1], sys.argv[2])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    reactor.callLater(30, update_topic, f)

    # run bot
    reactor.run()
