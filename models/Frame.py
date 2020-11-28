from copy import deepcopy
class Frame(object):

    def __init__(self, name, images=None):
        self.name = name
        if images == None:
            self.images = {}
        else:
            self.images = images

    def addOrUpdateImage(self, image):
        self.images[image.name] = image

    def hasImage(self, imageName):
        return imageName in self.images.keys()

    def __copy__(self):
        newOne = Frame(self.name)
        newOne.images = self.images
        return newOne

    def __deepcopy__(self, memodict={}):
        newOne = Frame(self.name)
        newOne.images = deepcopy(self.images)
        return newOne