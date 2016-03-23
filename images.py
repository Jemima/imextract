class Image:
    @classmethod
    def test(self, seq, offset):
        return seq[offset:offset + len(self.magic)] == self.magic


class Jpeg(Image):
    magic = [0xFF, 0xD8]

    @staticmethod
    def calculate_length(seq, offset):
        ''' Jpeg files consist of a bunch of markers,
            the exact marker format depends on the specific JPEG
            variant being used (JFIF is most common, EXIF is also an option).

            The first marker is always the Start of Image (SOI) marker 0xFF, 0xD8,
            following are any number of markers.
            Each marker has the format:
            0xFF, 0x?? - 2 byte marker type, always starts with 0xFF, 0x?? is not 0x00.
            0xAAAA - Optional 2 byte big-endian length of marker,
                     including this field but excluding marker type.
            ...    - 0xAAAA-2 bytes of marker data.
            ...    - 0 or more bytes of data. If 0xFF appears it will always be followed by 0x00.
            The last marker is the End of Image (EOI) marker 0xFF, 0xD9.

            This means our parse method is:
            1. Read 2-byte marker. If marker is EOI finish.
            2. Check if the next byte is 0xFF, if so assume it's a new marker and go to 1,
                otherwise continue.
            3. Read the 2-byte length.
            4. Skip ahead length-2 bytes.
            5. Read until the next marker (0xFF, 0x?? where ?? != 00) occurs.

            We have an extra check to make sure we really have a jpeg image:
            The two most common JPEG formats are JFIF and EXIF each of which
            requires a certain marker to be first, so check for those two markers.
            '''
        current = offset
        marker = seq[offset:offset+2]
        if marker != bytes([0xFF, 0xD8]):
            # Doesn't look like a JPEG image.
            print("No valid marker found")
            return 0
        current += 2

        marker = seq[current:current+2] + seq[current+4:current+9]
        if marker == bytes([0xFF, 0xE0, 0x4A, 0x46, 0x49, 0x46, 0x00]):
            # JFIF
            print("Found JPEG/JFIF")
            pass
        elif marker == bytes([0xFF, 0xE1, 0x45, 0x78, 0x69, 0x66, 0x00]):
            # EXIF
            print("Found JPEG/EXIF")
            pass
        else:
            # Unrecognised
            print("Not a recognised JPEG format")
            return 0

        # We made it this far, so it looks like a JPEG.
        # Begin the main parse loop.
        try:
            marker = seq[current:current+2]
            while marker != bytes([0xFF, 0xD9]) and marker != []:
                if seq[current+2] == 0xFF:
                    # Looks like a new marker just after
                    print("lengthless marker")
                    current += 2
                else:
                    # Skip to the end of the block
                    length = 0xFF * seq[current+2] + seq[current+3]
                    print("Skipping %d bytes" % (length+2))
                    current += length + 2

                    # Keep on searching until we hit what looks like the next block.
                    while seq[current] != 0xFF or seq[current+1] == 0x00:
                        current += 1

                marker = seq[current:current+2]
        except IndexError:
            # Reached the end of the file before finding a match,
            print("Couldn't find the end.")
            return 0

        # Found the end, return the length
        return current - offset + 2

types = [Jpeg]
