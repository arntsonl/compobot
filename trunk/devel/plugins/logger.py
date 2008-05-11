# system imports
import time, os

import base

class Plugin(base.Plugin):
    """
    A simple plugin that will store all messages sent.
    """

    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.done = False

        self.name = "logger"

        self.tot_logs = 0
        self.file = self.open_file()
        self.bot.reactor.callLater(60*60*24, self.move_log)

    def open_file(self):
        a, b = self.bot.prefs["logfile"].split(".")
        a = a + str(self.tot_logs)
        path = a+"."+b
        if os.path.isfile(path):
            x = path.split(".")[0]
            num = int(x[len(a)-1::])
            self.tot_logs = num + 1
            return open(a+str(self.tot_logs)+"."+b, "a")
        return open(path, "a")

    def move_log(self):
        self.file.write("---END FILE---")
        self.file.close()
        self.tot_logs += 1
        self.file = self.open_file()
        self.file.write("---BEGIN---")
        self.bot.reactor.callLater(60*60*24, self.move_log)

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
                self.log("[%s] <*ME*> %s" % (channel, msg))
        return None
