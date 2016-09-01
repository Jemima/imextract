#!/usr/bin/env python
''' Main file to actually search for and extract images from a blob.
'''
import argparse
import mmap
import os
import images
import build

def naive(blob, outfolder):
    count = 0
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
    return count

def aho_corasick(blob, outfolder):
    count = 0
    state = build.main(images.types)
    for n in range(0, len(blob)):
        while state.g(blob[n]) is None:
            state = state.f
        state = state.g(blob[n])
        if state.output:
            if images.image.Image.verbose:
                print("Found magic for " + str(state.output) +
                      " at " + str(n) + ", ")
            for t in state.output:
                # We're at the last character in the needle,
                # figure out the offset of the start of the blob
                offset = n - len(t.magic) + 1
                l = t.calculate_length(blob, offset)
                if l > 0:
                    name = outfolder + '/image' + str(count) + t.get_extension()
                    f = open(name, 'wb')
                    f.write(blob[offset:offset+l])
                    f.close()
                    print("Saved %d-byte image to %s" % (l, name))
                    count += 1
    return count

def main(infile, outfolder, algorithm):
    ''' Main function.
        Run matchers against the blob provided in args.
    '''
    try:
        # Windows-style, try opening as binary
        fd = os.open(infile, os.O_RDONLY | os.O_BINARY)
    except AttributeError:
        # We're probably missing O_BINARY e.g. on Linux,
        # so try opening without that flag.
        fd = os.open(args.infile, os.O_RDONLY)

    try:
        blob = mmap.mmap(fd, 0, access=mmap.PROT_READ)
        if algorithm == "aho-corasick":
            count = aho_corasick(blob, outfolder)
        elif algorithm == "naive":
            count = naive(blob, outfolder)
        print("Found " + str(count) + " matches")
    finally:
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
    parser.add_argument('--algorithm',
                        choices=['naive', 'aho-corasick'],
                        help='Which search algorithm to use, Aho-Corasick is the default')
    args = parser.parse_args()
    images.image.Image.verbose = args.verbose
    main(args.infile, args.outfolder, args.algorithm)
