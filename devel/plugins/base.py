
class Plugin(object):
    def __init__(self, bot, prefs):
        self.bot = bot

        self.prefs = prefs

        self.name = "base"

    def connect(self):
        """Called when our bot connects to the server."""
        pass

    def disconnect(self):
        """Called when our bot leaves the server."""
        pass

    def signon(self):
        """Called when bot has successfully signa onto the server."""
        pass

    def join(self, channel):
        """Called when bot joins channel."""
        pass

    def userjoin(self, user, channel):
        """Called when a new user joins the channel"""
        pass

    def nickmessage(self, user, channel, msg):
        """Called if the bot receies a message that contains our nick."""
        pass

    def privatemessage(self, user, channel, msg):
        """Called if someone sends our bot a private message."""
        pass

    def generalmessage(self, user, channel, msg):
        """Called if someone says something - and it isn't directed towards our bot."""
        pass

    def anymessage(self, user, channel, msg):
        """This will be called for any [msg, priv_msg, msg_with_name] that the bot gets.
           Use this if you don't need to distinguish messages."""
        pass

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        pass

    def usernickchange(self, old, new):
        """This gets when a user changes there nick."""
        pass

    def reactorchance(self, reactor):
        """This gets called when the bot gives us a chance to give a command to the reactor,
           such as a call to reactor.callLater."""
        pass
