import sys, os

defaultText = "\
# Competition Bot v0.1\n\
#   Credits to: RB[0], Cthulhu32, & Keeyai\n\
nick=CompoBot.v1\n\
channel=pitfall0\n\
server=irc.freenode.net\n\
port=6667\n\
logfile=pyweek_log1.txt\n"

validCmd = ["nick","channel","server","port","logfile"]

class Preferences:
    """
    A class used to load preferences, or create new ones
    if the default has not been set yet.
    """
    def __init__(self):
        self.file = "prefs.ini"
        self.data = {} # dictionary full of our data
        self.loadPreferencesFile(self.file)

    def loadPreferencesFile(self, filename):
        if not (os.path.exists(filename)):
            prefFile = open(filename, "w")
            prefFile.write(defaultText)
            prefFile.close()
        inFile = open(filename, "r")
        self.readPreferences(inFile)
        prefFile.close()

    def readPreferences(self, inFile):
        fileContent = inFile.readlines()
        for line in fileContent:
            if line[0] == "#":
                continue
            line=line.strip("\r\n")
            command, value = line.split("=")
            if command in validCmd:
                self.data[command] = value
        
        
