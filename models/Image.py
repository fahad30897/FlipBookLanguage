from copy import copy,deepcopy
class Image(object):
    def __init__(self, name, position, size, path):
        self.name = name
        self.position = position
        # self.frameNumber = frameNumber
        self.size = size
        self.path = path

    def resize(self, width, height):
        self.size.first = width
        self.size.second = height

    def updatePosition(self, x, y):
        self.position.first = x
        self.position.second = y

    def __copy__(self):
        newOne = Image(self.name, copy(self.position),copy(self.size),self.path)
        return newOne

    def __deepcopy__(self, memodict={}):
        newOne = Image(self.name, deepcopy(self.position),deepcopy(self.size),self.path)
        return newOne



