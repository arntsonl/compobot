import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)

    def privatemessage(self, user, channel, msg):
        cmd = msg.split()
        if cmd[0] == "DO": #make sure this is a command not just a message!
            cmd = cmd[1::]
            if len(cmd) >= 1 and cmd[0] == "QUIT":
                self.bot.msg(self.bot.channel, user+": Quit, eh?")
                if self.bot.password and len(cmd) == 2 and\
                   cmd[1] == self.bot.password:
                    self.bot.msg(self.bot.channel, "I die!")
                    self.bot.stop_serving()
                else:
                    self.bot.msg(self.bot.channel, "Wrong password!")
            return True
        return False
                
