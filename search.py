#!/usr/bin/env python
import sys
import argparse
import mmap
import os
import images


def main(args):
    try:
        # Windows-style, try opening as binary
        fd = os.open(args.infile, os.O_RDONLY | os.O_BINARY)
    except(AttributeError):
        # We're probably missing O_BINARY e.g. on Linux,
        # so try opening without that flag.
        fd = os.open(args.infile, os.O_RDONLY)

    blob = None
    try:
        blob = mmap.mmap(fd, 0, access=mmap.PROT_READ)
        print(images.types[0].calculate_length(blob, 0))

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

    args = parser.parse_args()
    main(args)
