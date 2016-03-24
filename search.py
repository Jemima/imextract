#!/usr/bin/env python
''' Main file to actually search for and extract images from a blob.
'''
import argparse
import mmap
import os
import images


def main(infile, outfolder):
    '''Main function.
        Run matchers against the blob provided in args.
    '''
    try:
        # Windows-style, try opening as binary
        fd = os.open(infile, os.O_RDONLY | os.O_BINARY)
    except AttributeError:
        # We're probably missing O_BINARY e.g. on Linux,
        # so try opening without that flag.
        fd = os.open(args.infile, os.O_RDONLY)

    blob = None
    count = 1
    try:
        blob = mmap.mmap(fd, 0, access=mmap.PROT_READ)
        for n in range(0, len(blob)):
            for t in images.types:
                l = t.calculate_length(blob, n)
                if l > 0:
                    name = outfolder + '/image' + str(count) + t.get_extension()
                    f = open(name, 'wb')
                    f.write(blob[n:n+l])
                    f.close()
                    print("Saved %d-byte image to %s" % (l, name))
                    count += 1


    finally:
        print(blob)
        if blob is not None:
            blob.close()
        os.close(fd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract images from a binary blob')
    parser.add_argument('-i',
                        '--infile',
                        type=str,
                        help='Input file',
                        required=True)
    parser.add_argument('-o',
                        '--outfolder',
                        type=str,
                        help='Output folder',
                        default='.')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Be extra verbose')
    args = parser.parse_args()
    images.image.Image.verbose = args.verbose
    main(args.infile, args.outfolder)
