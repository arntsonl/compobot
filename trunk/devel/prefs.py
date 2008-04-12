import sys, os

defaultText = "\
# Competition Bot v0.1\n\
#   Credits to: RB[0], Cthulhu32, & Keeyai\n\
nick=CompoBot.v1\n\
channel=pitfall0\n\
server=irc.freenode.net\n\
port=6667\n\
logfile=pyweek_log1.txt\n"

validCmd = ["nick","channel","server","port",
            "logfile","plugins","password"]

class Preferences(object):
    """
    A class used to load preferences, or create new ones
    if the default has not been set yet.
    """
    def __init__(self):
        self.file = "prefs.ini"
        self.data = {} # dictionary full of our data
        self.loadPreferencesFile(self.file)

        self.data["port"] = int(self.data["port"])

    def loadPreferencesFile(self, filename):
        if not (os.path.exists(filename)):
            prefFile = open(filename, "w")
            prefFile.write(defaultText)
            prefFile.close()
        inFile = open(filename, "r")
        self.readPreferences(inFile)
        inFile.close()

    def get_value(self, val):
        if val[0] == '"' and val[-1] == '"':
            return val[1:-1]
        else:
            try:
                a = float(val)
                try:
                    if int(val) == a:
                        a = int(val)
                except:
                    pass
                return a
            except:
                return val
        return "Strange!!! - was val: %s"%val

    def get_list(self, value, f, lineN):
        num = 0
        cur = value
        for line in f:
            if num-1 > lineN:
                if line[0] == "#":
                    continue
                line=line.strip("\r\n")

                cur = cur + line

                if line[-1] == "]": #end list
                    break
            num += 1

        values = cur[1:-1].split(",")
        for i in xrange(len(values)):
            values[i] = values[i].strip()

        ret = []
        for i in values:
            ret.append(self.get_value(i))
        return ret, num+1

    def readPreferences(self, inFile):
        fileContent = inFile.readlines()
        lineN = 0
        line_skip = 0
        for line in fileContent:
            if lineN<= line_skip:
                lineN += 1
                continue
            if line[0] == "#":
                continue
            line=line.strip("\r\n")
                
            command, value = line.split("=")
            if value[0] == "[":
                value, line_skip = self.get_list(value, fileContent, lineN)
            else:
                value = self.get_value(value)
            if command in validCmd:
                self.data[command] = value
            lineN += 1
a = Preferences()
print a.data
        
