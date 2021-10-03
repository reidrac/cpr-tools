#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path
import struct

__version__ = "1.0"


def main():

    parser = ArgumentParser(description="CPR dumper for CPC+ cartridges",
                            epilog="Copyright (C) 2021 Juan J Martinez <jjm@usebox.net>",
                            )

    parser.add_argument("--version", action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument("-d", "--directory", dest="dir", default=".", type=str,
                        help="output directory (default: .)")
    parser.add_argument("file", help="file to dump")

    args = parser.parse_args()

    with open(args.file, "rb") as fd:
        data = fd.read()

    if data[:4] != b"RIFF":
        parser.error("Not a RIFF file")

    size = struct.unpack_from("<I", data[4:8])[0]
    if size != len(data) - 8:
        parser.error("RIFF length (%d) doesn't match CPR size (%d)" %
                     (size, len(data) - 8))

    if data[8:12].lower() != b"ams!":
        parser.error("AMS! form-type not found")

    i = 12
    cnt = 0
    while i < len(data):
        size = struct.unpack_from("<I", data[i+4:i+8])[0]
        i += 8
        chunk_filename = path.join(
            args.dir, "%s.%02d.bin" % (path.basename(args.file), cnt))
        if size == 0:
            print("Skipping empty chunk %02d" % cnt)
            continue
        print("Writing chunk %s (%d bytes)" % (chunk_filename, size))
        with open(chunk_filename, "wb") as fd:
            fd.write(data[i:i+size])
        i += size
        cnt += 1
    print("Dumped %d chunks" % cnt)

    return 0


if __name__ == "__main__":
    main()
