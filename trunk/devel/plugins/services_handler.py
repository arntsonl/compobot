import base

class Plugin(base.Plugin):
    def __init__(self, bot, prefs):
        base.Plugin.__init__(self, bot, prefs)

        self.name = "services handler"

        self.email = self.prefs["reg_email"]
        self.password = self.prefs["reg_pass"]

    def from_services(self, user, channel, msg):
        if user == "NickServ":
            return True
        if channel == "AUTH":
            return True
        if user == "ChanServ":
            return True
        if user == "":#this obviously better be from services!
            return True
        return False

    def login(self):
        if self.password:
            self.bot.msg(self.bot.channel, "/msg NickServ IDENTIFY %s"%self.password)
        else:
            print "no <password>!"

    def register(self):
        if self.password:
            self.bot.msg(self.bot.channel, "/msg NickServ register %s"%self.password)
            if self.email:
                self.bot.msg(self.bot.channel, "/msg NickServ set hide email on")
                self.bot.msg(self.bot.channel, "/msg NickServ set email %s"%self.email)
            else:
                print "no <email>"
            self.login()
        else:
            print "no <password>!"

    def anymessage(self, user, channel, msg):
        if self.from_services(user, channel, msg): #check this is from services!
            print "Serv:", [msg]
            if msg == "If this is your nickname, type /msg NickServ IDENTIFY <password>":
                self.login()
            if "The nickname" in msg and\
               self.prefs["nick"] in msg and\
               "is not registered" in msg:
                self.register()
            return True
        return False

        
