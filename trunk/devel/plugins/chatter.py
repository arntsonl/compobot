import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)
        self.take_command = False #this makes sure we don't respond to commands
        #command_parser should handle that!
        #if you aren't running command_parser though - you can turn this to True

        self.msg_from_users = {} #a little bit of niceness ;)
        self.all_msgs = [["I am just a bot", 2],
                         ['Hello? I said - "I am just a bot" - do you understand?', 3],
                         ["You don't understand then - stop talking to me!", 4],
                         ["You are starting to make me pay more attention to you than I should - good day...", 5],
                         ["...I am ignoring you now", 6],
                         ["...", None]]

    def get_message(self, user):
        if user:
            if not user in self.msg_from_users:
                self.msg_from_users[user] = 0
            for i in self.all_msgs:
                if not i[1] == None:
                    if self.msg_from_users[user] <= i[1]:
                        self.msg_from_users[user] += 1
                        return user+": "+i[0]
                    else:
                        pass
                else:
                    return user+": "+i[0]
        return ""

    def priv_msg(self, user, channel, msg):
        if (not msg.split()[0] == "DO") and\
           (self.take_command == False):
            if not user == self.bot.username: #check we aren't talking to ourself!
            self.bot.msg(self.bot.channel, self.get_message(user))

    def msg_with_name_in_it(self, user, channel, msg):
        if (not msg.split()[0] == "DO") and\
           (self.take_command == False):
            if not user == self.bot.username: #check we aren't talking to ourself!
            self.bot.msg(self.bot.channel, self.get_message(user))

        
