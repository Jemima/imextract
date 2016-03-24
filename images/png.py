'''Png extraction
'''
from .image import Image
import struct


class Png(Image):
    ''' Match a png.
    '''
    magic = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]

    @staticmethod
    def get_extension():
        return ".png"

    @staticmethod
    def get_magic():
        return Png.magic

    @staticmethod
    def calculate_length(seq, offset):
        ''' Png files consist of a bunch of markers,
            after the header the first marker is always IHDR,
            followed by any number of chunks,
            then the last chunk is IEND of length 0.
            Each chunk consists of:
            4 bytes of length
            4 bytes of type
            length bytes of data
            4 bytes of CRC.

            To read we read the header, check the first chunk is IHDR,
            then skip chunk by chunk until we reach IEND.
        '''
        current = offset
        marker = seq[offset:offset+len(Png.magic)]
        if marker != bytes(Png.magic):
            # Doesn't look like a PNG image.
            # if Image.verbose:
            #     print("No valid marker found")
            return 0
        current += len(Png.magic)

        try:
            while True:
                length = struct.unpack(">I", seq[current:current+4])[0]
                current += 4
                marker = seq[current:current+4]
                current += 4
                current += length + 4
                if Image.verbose:
                    print("Found chunk %s" % marker.decode())
                if marker == "IEND".encode():
                    return current - offset
        except struct.error:
            # Looks like we hit the end of our blob
            # before finding the end chunk,
            # probably not a PNG after all.
            return 0
