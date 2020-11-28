
class Pair(object):

    def __init__(self,first ,second):
        self.first = first
        self.second = second

    def __copy__(self):
        newOne = type(self)(self.first, self.second)

        return newOne

    def __deepcopy__(self, memodict={}):
        newOne = type(self)(self.first, self.second)
        return newOne
