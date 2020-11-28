from models.Image import Image
from models.Frame import Frame
from models.Pair import Pair

class State(object):

    def __init__(self, outputFile, outputType, resolution=100, duration=400, loop=0):
        self.symbolTable = [] # Maintain a nested symbol table having mappings from identifer names to values
        self.currLevel = 0 # current nesting level
        self.symbolTable.append({}) # initialize level zero
        self.outputType = outputType # command line arg (pdf/gif)
        self.outputFile = outputFile # command line arg (path to file where output will be stored)
        self.flipBook = [] # List of frames. These frames will finally be converted to flipbool
        self.duration = duration
        self.loop = loop
        self.resolution = resolution
        self.defaultFrameSize = Pair(640,480) # TODO: Make this customizable
        self.red = 250 # TODO: Make initiali background color customizable
        self.blue = 250
        self.green = 250

    """
        checks if given identifier name has been used at current and ancestor nesting levels
    """
    def hasIdentifier(self, ident):
        for i in range(0, self.currLevel +1):
            if ident in self.symbolTable[i].keys():
                return True
        return False

    """
        sets the given value for identifier. First checks if the identifier exists at current or ancestor nesting levels.
        If so update it. Else create new variable at current nesting level.
    """
    def setIdentifier(self, ident, value):
        # self.symbolTable[self.currLevel][ident] = value
        found = False
        for i in range(0 , self.currLevel + 1):
            if ident in self.symbolTable[i].keys():
                self.symbolTable[i][ident] = value
                found = True

        if not found:
            self.symbolTable[self.currLevel][ident] = value

    """
        Fetch the value of given identifer from current or ancestor nesting levels
    """
    def getIdentifier(self, ident):
        for i in range(0 , self.currLevel + 1):
            if ident in self.symbolTable[i].keys():
                return self.symbolTable[i][ident]

    """
        Adds frame to flipbook (obviously)
    """
    def addFrameToFlip(self, frame):
        self.flipBook.append(frame)

    """
        Increment the nesting level and initialize the dict at that level
    """
    def incLevel(self):
        self.symbolTable.append({})
        self.currLevel += 1

    """
        Decrements the nesting level. All variables created inside that level (block) will be lost.
    """
    def decLevel(self):
        self.symbolTable[self.currLevel].clear()
        self.currLevel -= 1