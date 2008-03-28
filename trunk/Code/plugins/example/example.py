"""

    example.py

    @summary: example plugin for CompoBot

    To Create a Plugin:
        A CompoBot plugin requires two files, a folder and a .py file inside that
        folder with the same name. Inside the .py file, there should be a class
        called plugin (see below) with a register method. That's it!

        CompoBot will go through all the folders in the plugins directory,
        try to import the file with the same name as the folder, instantiates
        the plugin class, and calls its register method with the bot as a parameter.
        The register method should handle everything the plugin needs to be
        effective -- usually a series of calls to bot.registerCallback.

        See the CompoBot docstring for examples of all the events and the
        parameters that go with them.

        FYI, You can print from inside the plugin and it will be logged automatically.
"""

class plugin:

    def register(self, bot):
        """Registers the plugin. Saves the bot for easy access. Called when
        the plugin is loaded."""
        self.bot = bot

        # register our callbacks
    #    bot.registerCallback('generalmessage', self.test)
        bot.registerCallback('nickmessage', self.respond)

    def test(self, *args):
        print 'Test'    # this gets logged
        self.bot.msg(self.bot.channel, 'plugin test')

    def respond(self, user, channel, message):
        self.bot.msg(channel, "%s: I'm just a bot. A CompoBot!" % user)
