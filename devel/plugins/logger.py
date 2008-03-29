# system imports
import time

import base

class MessageLogger(base.Plugin):
    """
    A simple plugin that will store all messages sent.
    """

    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.file = open(prefs["logfile"], "a")
        self.done = False

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()
        self.done = True

    def any_msg(self, user, channel, msg):
        if not self.done:
            self.log("[%s] <%s> %s" % (channel, user, msg))
        return None
