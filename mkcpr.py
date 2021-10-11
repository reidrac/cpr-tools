#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path
import struct

__version__ = "1.0.3"

DEF_OUT = "out.cpr"


def main():

    parser = ArgumentParser(description="Make CPR for CPC+ cartridges",
                            epilog="Copyright (C) 2021 Juan J Martinez <jjm@usebox.net>",
                            )

    parser.add_argument("--version", action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument("-o", dest="output",
                        help="output file (default: %s)" % DEF_OUT, type=str, default=DEF_OUT)
    parser.add_argument("-s", "--sort", dest="sort", action="store_true",
                        help="sort input file alphabetically")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
                        help="overwrite destination if already exists")
    parser.add_argument("-r", "--raw", dest="raw", action="store_true",
                        help="don't include header information")
    parser.add_argument("-p", "--pad", dest="pad", action="store_true",
                        help="pad chunks to 16K")
    parser.add_argument("files", help="files to include as chunks", nargs="+")

    args = parser.parse_args()

    files = args.files
    if args.sort:
        files = sorted(files)

    data = []
    for file in files:
        with open(file, "rb") as fd:
            bank = fd.read()
        if len(bank) > 16 * 1024:
            parser.error("%s: bank size is more than 16K" % file)
        data.append(bank)

    if len(data) > 32:
        parser.error("More than 32 chunks")

    chunks = len(data)
    if len(data) < 32:
        for _ in range(32 - len(data)):
            data.append([])

    if args.pad:
        for i in range(32):
            if len(data[i]) != 16 * 1024:
                extended = list(data[i]) + \
                    [0 for _ in range(16 * 1024 - len(data[i]))]
                data[i] = bytes(extended)

    if path.exists(args.output) and not args.force:
        parser.error("%s: file already exists" % args.output)

    # (block size + chunk header) x block + 4 ("AMS!")
    total_size = sum([len(block) + 8 for block in data]) + 4
    with open(args.output, "wb") as fd:
        if not args.raw:
            fd.write(b"RIFF")
            fd.write(struct.pack("<I", total_size))
            fd.write(b"AMS!")

        for i, bank in enumerate(data):
            if not args.raw:
                fd.write(b"cb%02d" % i)
                fd.write(struct.pack("<I", len(bank)))
            if bank:
                fd.write(bank)

    print("Generated %s (%d chunks%s), %d bytes" % (
        args.output,
        chunks,
        "" if chunks == 32 else ", padded to 32",
        total_size + 8
    ))

    return 0


if __name__ == "__main__":
    main()
