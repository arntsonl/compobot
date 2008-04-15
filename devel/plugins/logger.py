# system imports
import time

import base

class Plugin(base.Plugin):
    """
    A simple plugin that will store all messages sent.
    """

    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.file = open(prefs["logfile"], "a")
        self.done = False

        self.name = "logger"

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()
        self.done = True

    def anymessage(self, user, channel, msg):
        if not self.done:
            if not user == self.bot.username:
                self.log("[%s] <%s> %s" % (channel, user, msg))
            else:
                self.log("[%s] <~~To Me> %s" % (channel, msg))
        return None
