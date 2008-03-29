import base

class CommandParser(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)

    def priv_msg(self, user, channel, msg):
        if msg[0] == "!":
            msg = msg[1::]
            cmd = msg.split()
            if cmd == ["QUIT"]:
                self.bot.stop_serving()
