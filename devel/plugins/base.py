
class Plugin(object):
    def __init__(self, bot, prefs):
        self.bot = bot

        self.prefs = prefs

    def connect(self):
        """Called when our bot connects to the server."""
        pass

    def close(self):
        """Called when our bot leaves the server."""
        pass

    def signed_on(self):
        """Called when bot has successfully signa onto the server."""
        pass

    def join(self, channel):
        """Called when bot joins channel."""
        pass

    def msg_with_name_in_it(self, user, channel, msg):
        """Called if the bot receies a message that contains our nick."""
        pass

    def priv_msg(self, user, channel, msg):
        """Called if someone sends our bot a private message."""
        pass

    def msg(self, user, channel, msg):
        """Called if someone says something - and it isn't directed towards our bot."""
        pass

    def any_msg(self, user, channel, msg):
        """This will be called for any [msg, priv_msg, msg_with_name] that the bot gets.
           Use this if you don't need to distinguish messages."""
        pass

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        pass

    def change_nick(self, old, new):
        """This gets when a user changes there nick."""
        pass

    def reactor_chance(self, reactor):
        """This gets called when the bot gives us a chance to give a command to the reactor,
           such as a call to reactor.callLater."""
        pass
