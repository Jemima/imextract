'''Module containing the image matching parent class.
'''
import abc


class Image(metaclass=abc.ABCMeta):
    '''Whether or not to be verbose.
    '''
    verbose = False
    '''Parent class for the image matchers.
    '''
    @staticmethod
    @abc.abstractmethod
    def get_extension():
        '''Returns the extension for this type of image.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def get_magic():
        '''Returns a sequence of bytes which can serve as an identifier
            for this type.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def calculate_length(seq, offset):
        '''Tries to find an image at the specified offset
            in seq. Returns 0 if no image was found, the length of the image otherwise.
        '''
        pass
