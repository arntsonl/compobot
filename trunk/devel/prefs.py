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
            "logfile","plugins","password",
            "reg_email", "reg_pass"]

class ListStack(object):
    def __init__(self):

        self.stack = [[]]

        self.closed_stacks = []

    def value(self, val):
        self.get_current_stack().append(val)

    def push(self):
        self.stack.append([])

    def pop(self):
        self.closed_stacks.append(self.get_num_stack())

    def get_current_stack(self):
        a = []
        for i in xrange(len(self.stack)):
            i = len(self.stack) - i - 1
            if not i in self.closed_stacks:
                return self.stack[i]
        return []

    def get_num_stack(self):
        return self.stack.index(self.get_current_stack())

    def get_finished_stack(self):
        new = []
        for i in xrange(len(self.stack)):
            if i == 0:
                new.extend(self.stack[i])
            else:
                new.append(self.stack[i])
        return new

class Preferences(object):
    """
    A class used to load preferences, or create new ones
    if the default has not been set yet.
    """
    def __init__(self):
        self.file = "prefs.ini"
        self.data = {} # dictionary full of our data
        self.loadPreferencesFile(self.file)

        for i in validCmd:
            if not i in self.data:
                self.data[i] = None

    def loadPreferencesFile(self, filename):
        if not (os.path.exists(filename)):
            prefFile = open(filename, "w")
            prefFile.write(defaultText)
            prefFile.close()
        inFile = open(filename, "r")
        self.readPreferences(inFile)
        inFile.close()

    def get_value(self, val):
        if val == "None":
            return None
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

        stack = ListStack()
        for i in values:
            if i[0] == "[":
                stack.push()
                if i[-1] == "]":
                    stack.value(self.get_value(i[1:-1]))
                    stack.pop()
                else:
                    stack.value(self.get_value(i[1::]))
            else:
                if i[-1] == "]":
                    stack.value(self.get_value(i[0:-1]))
                    stack.pop()
                else:
                    stack.value(self.get_value(i))
        values = stack.get_finished_stack()
        return values, num+1

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
            if not value:
                value = "None"
            if not command:
                command = None
            if value[0] == "[":
                value, line_skip = self.get_list(value, fileContent, lineN)
            else:
                value = self.get_value(value)
            if command in validCmd:
                self.data[command] = value
            lineN += 1
