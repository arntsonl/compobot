import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)

    def priv_msg(self, user, channel, msg):
        if msg[0] == "$":
            msg = msg[1::]
            cmd = msg.split()
            if cmd[0] == "QUIT":
##                self.bot.msg(self.bot.channel, user+": Quit, eh?")
                if self.bot.password and len(cmd) == 2 and\
                   cmd[1] == self.bot.password:
##                    self.bot.msg(self.bot.channel, "I die!")
                    self.bot.stop_serving()
                else:
##                    self.bot.msg(self.bot.channel, "Wrong password!")
                    pass
                
