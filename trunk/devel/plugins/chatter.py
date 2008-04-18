import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)

        self.msg_from_users = {} #a little bit of niceness ;)
        self.all_msgs = [["I am just a bot", 0],
                         ['Hello? I said - "I am just a bot" - do you understand?', 1],
                         ["You don't understand then - stop talking to me!", 2],
                         ["You are starting to make me pay more attention to you than I should - good day...", 3],
                         ["...I am ignoring you now", 4],
                         ["...", None]]

        self.name = "chatter"

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

    def privatemessage(self, user, channel, msg):
        if not user == self.bot.username: #check we aren't talking to ourself!
            self.bot.msg(self.bot.channel, self.get_message(user))
            return True
        return False

    def nickmessage(self, user, channel, msg):
        if not user == self.bot.username: #check we aren't talking to ourself!
            self.bot.msg(self.bot.channel, self.get_message(user))
            return True
        return False

        
