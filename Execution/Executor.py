from models.Frame import Frame
from models.Image import Image
from models.Pair import Pair
from copy import copy,deepcopy
import sys

class Executor(object):

    def __init__(self, state, imageProcessor):
        self.state = state
        self.imageProcessor = imageProcessor
        self.lineNo = 1

    def setLineNo(self, number):
        self.lineNo = number
    """
        Checks if given Identifier is of primitive type ( number or string).    
    """
    def checkIfPrimitive(self, ident):
        if not self.state.hasIdentifier(ident):
            self.abort("Identifier used before declaration - " + str(ident))
        var = self.state.getIdentifier(ident)
        if isinstance(var, float) or isinstance(var, str) or isinstance(var, int):
            return True
        return False

    """
        Fetches value associated with given identifier from the symbol table.
    """
    def getPrimitiveValue(self, ident):
        if not self.state.hasIdentifier(ident):
            self.abort("Identifier used before declaration - " + str(ident))
        return self.state.getIdentifier(ident)

    """
        Declares a variable for the given identifier.
    """
    def declareVariable(self, ident):
        if self.state.hasIdentifier(ident):
            self.abort("Identifier redeclared - " + str(ident))
        self.state.setIdentifier(ident, "")

    """
        Assigns the value to given identifier.
    """
    def assignIdentifier(self, ident, value):
        if not self.state.hasIdentifier(ident):
            self.abort("Identifier used before declaration - " + str(ident))
        self.state.setIdentifier(ident, value)

    """
        Creates an Image object using the given path and assigns it to given identifier
    """
    def createImage(self, ident, path):
        if self.state.hasIdentifier(ident):
            self.abort("Identifier redeclared - " + ident)
        newImage = Image(ident,Pair(0,0), self.imageProcessor.getSize(path), path)
        self.state.setIdentifier(ident, newImage)

    """
        Updates the size of image identifier by give identifier
    """
    def resizeImage(self, ident, typ, width, height):
        if not self.state.hasIdentifier(ident):
            self.abort("Identifier used before declaration - " + str(ident))
        img = self.state.getIdentifier(ident)
        if not isinstance(img, Image):
            self.abort("Only images can be resized. Resize call on - " + str(ident))
        if typ == "MULT":
             img.resize(img.size.first * width, img.size.second * height)
             self.state.setIdentifier(ident, img)
        else:
            img.resize(width, height)
            self.state.setIdentifier(ident, img)

    """
        Creates a frame object and assigns it to given identifier
    """
    def createFrame(self, ident):
        if self.state.hasIdentifier(ident):
            self.abort("Identifier redeclared - " + ident)
        newFrame = Frame(ident)
        self.state.setIdentifier(ident, newFrame)

    """
        Deepcopies content of frame represented by ident1 to that by ident2
    """
    def copyFrame(self, ident1, ident2):
        if not self.state.hasIdentifier(ident1):
            self.abort("Identifier used before declaration - " + str(ident1))
        if not self.state.hasIdentifier(ident2):
            self.abort("Identifier used before declaration - " + str(ident2))
        srcFrame = self.state.getIdentifier(ident1)
        destFrame = self.state.getIdentifier(ident2)
        if not isinstance(srcFrame, Frame) or not isinstance(destFrame, Frame):
            self.abort("Only Frames can be copied. Copy called for " + str(ident1) + ", "  + str(ident2))

        destFrame = deepcopy(srcFrame)
        self.state.setIdentifier(ident2, destFrame)

    """
        Adds the given frame to flipbook
    """
    def addFrame(self, frame):
        if not self.state.hasIdentifier(frame):
            self.abort("Identifier used before declaration - " + str(frame))

        frameVal = self.state.getIdentifier(frame)
        if not isinstance(frameVal, Frame):
            self.abort("Only Frames can be added to Flipbook. Occured while ADDFRAME : " + str(frame))
        self.state.addFrameToFlip(deepcopy(frameVal))

    """
        Adds the given image to given frame at position (x,y)
    """
    def addImageToFrame(self, img, frame, x, y):
        if not self.state.hasIdentifier(frame):
            self.abort("Identifier used before declaration - " + str(frame))
        if not self.state.hasIdentifier(img):
            self.abort("Identifier used before declaration - " + str(img))
        if not isinstance(x, float) or not isinstance(y,float):
            self.abort("position must be int or float. Error in ADDIMAGETOFRAME with positions " + str(x) + ", " + str(y))
        imgVal = self.state.getIdentifier(img)
        frameVal = self.state.getIdentifier(frame)

        if not isinstance(imgVal,Image) or not isinstance(frameVal,Frame):
            self.abort("Only Images can be added to Frame. Occurred while ADDIMAGETOFRAME: " + str(img) + ", " +str(frame))

        imgValCopy = deepcopy(imgVal)
        imgValCopy.updatePosition(x, y)
        frameVal.addOrUpdateImage(imgValCopy)
        self.state.setIdentifier(frame, frameVal)

    """
        saves the image represented by object img at given path
    """
    def saveImage(self, img, path):
        if not self.state.hasIdentifier(img):
            self.abort("Identifier used before declaration - " + str(img))
        imgVal = self.state.getIdentifier(img)
        if not isinstance(imgVal,Image):
            self.abort("Only Images can be saved. Occurred while SAVEIMAGE: " + str(img))
        self.imageProcessor.saveImage(imgVal, path)

    """
        Fetches the size of image represented by img and assigns it in x and y
    """
    def getImageSize(self, img, x,y):
        if not self.state.hasIdentifier(img):
            self.abort("Identifier used before declaration - " + str(img))
        imgVal = self.state.getIdentifier(img)
        if not isinstance(imgVal,Image):
            self.abort("First Argumemnt of Get image size must be an image.")
        imgSize = imgVal.size
        self.state.setIdentifier(x, imgSize.first)
        self.state.setIdentifier(y, imgSize.second)

    """
        Core method that generates and saves the flipbook using the state variable.
    """
    def genereateFlip(self):
        flipBook = self.state.flipBook
        frameList = []
        for i in range(len(flipBook)):
            frame = flipBook[i]
            canvas = self.imageProcessor.getBlank(self.state.defaultFrameSize, self.state.red, self.state.blue, self.state.green)
            for imageItem in frame.images.items():
                canvas = self.imageProcessor.modifyAndAdd(canvas, imageItem[1])
            frameList.append(canvas)
        self.imageProcessor.saveFlipBook(frameList, self.state.outputFile, self.state.outputType,
                                         resolution=self.state.resolution, duration=self.state.duration,
                                         loop=self.state.loop)

    """
        Starts the loop by incrementing the nesting level.
    """
    def startLoop(self, loopVar, start,end):
        if not isinstance(start, int) or not isinstance(end, int):
            self.abort("Loop bound must be int (floats will be truncated)")
        self.state.incLevel()
        self.state.setIdentifier(loopVar, start)

    """
        Refreshes the loop block by clear previously saved loop local variables
    """
    def incLoop(self, loopVar):
        val = self.state.getIdentifier(loopVar)
        self.state.decLevel()
        self.state.incLevel()
        self.state.setIdentifier(loopVar,val+1)

    """
        Decrements the nesting level to end the loop
    """
    def endLoop(self):
        self.state.decLevel()

    def printStatement(self, string):
        print(str(string))

    def abort(self,msg):
        sys.exit("Logic Error. "+ msg + " at " +str(self.lineNo))