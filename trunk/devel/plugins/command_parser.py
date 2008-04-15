import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.name = "command_parser"

    def privatemessage(self, user, channel, msg):
        cmd = msg.split()
        if cmd[0] == "DO": #make sure this is a command not just a message!
            cmd = cmd[1::]
            if len(cmd) >= 1:
                if cmd[0] == "QUIT":
                    self.bot.msg(self.bot.channel, user+": Quit, eh?")
                    if self.bot.password and len(cmd) == 2 and\
                       cmd[1] == self.bot.password:
                        self.bot.msg(self.bot.channel, "I die!")
                        self.bot.stop_serving()
                    else:
                        self.bot.msg(self.bot.channel, "Wrong password!")
                elif cmd == ["GET", "PLUGINS"]:
                    n = ", ".join([i.name for i in self.bot.plugins])
                    self.bot.msg(self.bot.channel, "Plugins: "+n)
                elif cmd == ["GET", "PLUGINS", "PRIORITY"]:
                    n = []
                    for i in self.bot.plugin_list.descriptors:
                        n.append([i[0].name, i[1]])
                    s = ", ".join([(i[0] + " " + "{" + str(i[1]) + "}") for i in n])
                    self.bot.msg(self.bot.channel, "Plugins {Priority}: "+s)
                elif len(cmd) >= 4 and\
                     cmd[0] == "LOAD" and cmd[1] == "PLUGIN":
                    self.bot.register_plugin([cmd[2], int(cmd[3])])
                elif len(cmd) >= 3 and\
                     cmd[0] == "UNLOAD" and cmd[1] == "PLUGIN":
                    self.bot.remove_plugin(cmd[2])
                elif len(cmd) >= 4 and\
                     cmd[0] == "SET" and cmd[1] == "PRIORITY":
                    self.bot.reprioritize(cmd[2], int(cmd[3]))
            return True
        return False
                
