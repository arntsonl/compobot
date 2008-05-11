import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.name = "command_parser"

        self.admin = []

    def respond_help(self, user, channel, msg):
        cmd = msg.split()
        if cmd and cmd[0] == "HELP":
            if len(cmd) >= 2 and cmd[1] == "commands":
                self.bot.msg(self.bot.channel, "How to command me:")
                self.bot.msg(self.bot.channel, "All commands must be sent as a private message to me")
                self.bot.msg(self.bot.channel, "like: '/msg botname'")
                self.bot.msg(self.bot.channel, "The first command you must always do, for me to understand you, is 'DO'")
                self.bot.msg(self.bot.channel, "So a command looks like this:")
                self.bot.msg(self.bot.channel, " /msg botname DO COMMAND args")
                self.bot.msg(self.bot.channel, "Commands:")
                self.bot.msg(self.bot.channel, "IDENTIFY password")
                self.bot.msg(self.bot.channel, "QUIT")
                self.bot.msg(self.bot.channel, "GET PLUGINS")
                self.bot.msg(self.bot.channel, "GET PLUGINS PRIORITY")
                self.bot.msg(self.bot.channel, "LOAD PLUGIN pluginname priority")
                self.bot.msg(self.bot.channel, "UNLOAD PLUGIN pluginname")
                self.bot.msg(self.bot.channel, "SET PRIORITY pluginname new_priority")
                self.bot.msg(self.bot.channel, "SET PRIORITY pluginname new_priority")
                self.bot.msg(self.bot.channel, "These should be pretty self explanatory - but if not...")
                self.bot.msg(self.bot.channel, "...a better help command should be available soon!!!")
                self.bot.msg(self.bot.channel, "Good luck!")
            elif len(cmd) == 1:
                self.bot.msg(self.bot.channel, "to ask for help about commands, type:")
                self.bot.msg(self.bot.channel, "HELP commands")
            else:
                return False
            return True
        return False

    def nickmessage(self, user, channel, msg):
        return self.respond_help(user, channel, msg)

    def privatemessage(self, user, channel, msg):
        if self.respond_help(user, channel, msg):
            return True
        cmd = msg.split()
        if cmd[0] == "DO": #make sure this is a command not just a message!
            cmd = cmd[1::]
            if user in self.admin:
                if len(cmd) >= 1:
                    if cmd[0] == "QUIT":
                        self.bot.msg(self.bot.channel, user+": Quit, eh?")
                        self.bot.msg(self.bot.channel, "I die!")
                        self.bot.stop_serving()
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
            elif len(cmd) >= 2 and\
               cmd[0] == "IDENTIFY" and cmd[1] == self.bot.password:
                if not user in self.admin:
                    self.admin.append(user)
                    self.bot.msg(self.bot.channel, "Thank you for identifying yourself.")
                    self.bot.msg(self.bot.channel, "What do you want me to do?")
            else:
                self.bot.msg(self.bot.channel, "Ha! You have no tidentified yourself to me  yet")
                self.bot.msg(self.bot.channel, "Please send me the command:")
                self.bot.msg(self.bot.channel, "DO IDENTIFY <password>")
                self.bot.msg(self.bot.channel, "that way I know you have permission to do this.")
            return True
        return False
                
