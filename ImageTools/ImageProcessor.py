from PIL import Image
from models.Pair import Pair
import sys

class ImageProcessor(object):

    """
        Get the actual size of image.
    """
    def getSize(self, path):
        try:
            img = Image.open(path)
            return Pair(img.size[0], img.size[1])
        except Exception as e:
            if hasattr(e, 'message'):
                self.abort(e.message)
            else:
                self.abort(str(e))

    """
        Save the image at the given path
    """
    def saveImage(self,img, path):
        try:
            imgPIL = Image.open(img.path)
            imgPIL = imgPIL.resize((int(img.size.first), int(img.size.second)))
            imgPIL.save(path)
        except Exception as e:
            if hasattr(e, 'message'):
                self.abort(e.message)
            else:
                self.abort(str(e))
    """
        Creates a blank image/canvas with background color specified by red, blue green and returns it.
    """
    def getBlank(self, size, red, blue, green):
        try:
            return Image.new('RGB', (int(size.first), int(size.second)), (red, blue, green))
        except Exception as e:
            if hasattr(e, 'message'):
                self.abort(e.message)
            else:
                self.abort(str(e))

    """
        Loods the image specified by image.path, updates its size to image.size and add it to canvas at image.position
    """
    def modifyAndAdd(self, canvas, image):
        try:
            imgPIL = Image.open(image.path)
            imgPIL = imgPIL.resize((int(image.size.first),int(image.size.second)))
            canvas.paste(imgPIL, (int(image.position.first), int(image.position.second)))
            return canvas
        except Exception as e:
            if hasattr(e, 'message'):
                self.abort(e.message)
            else:
                self.abort(str(e))

    """
        Core method. Saves the given frameList in format specified by fileType.
    """
    def saveFlipBook(self, frameList, fileName, fileType, duration=None, loop=None,resolution=None):
        try:
            # print("image " , loop)
            if len(frameList) == 1:
                if fileType == "PDF":
                    frameList[0].save(fileName, format="PDF", resolution=resolution, save_all=True)
                else:
                    frameList[0].save(fileName, format='GIF', duration=duration, loop=loop, save_all=True)
            if fileType == "PDF":
                frameList[0].save(fileName, "PDF", resolution=resolution, save_all=True, append_images=frameList[1:])
            else:
                frameList[0].save(fileName, format='GIF', duration=duration, loop=loop, save_all=True, append_images=frameList[1:])
        except Exception as e:
            if hasattr(e, 'message'):
                self.abort(e.message)
            else:
                self.abort(str(e))

    def abort(self,msg):
        sys.exit("Image error. " + msg)



