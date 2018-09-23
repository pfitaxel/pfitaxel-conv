#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018  Érik Martin-Dorel
#
# JSON to "learn-ocaml exercise dir" format converter
#
# Licensed under BSD-3 <https://opensource.org/licenses/BSD-3-Clause>
#
# Report bugs to <https://github.com/pfitaxel/pfitaxel-conv/issues>

import getopt
import json
import os
import sys

version = "0.1.0"

# Default values
json_file = ""
exo_dir = ""


def usage(exitcode):
    print("Usage:")
    print("\t%s -h" % os.path.basename(__file__))
    print("\t%s -o <dest exo dir> <src JSON file>"
          % os.path.basename(__file__))
    print("\t# where <dest exo dir> is the path of the dir to be created.\n")
    print("Summary:")
    print("\tJSON to 'learn-ocaml exercise dir' format converter\n")
    print("Example:")
    print("\t%s -o ./repo/ex1/ ./ex1.json" % os.path.basename(__file__))
    exit(exitcode)


def args_parse(argv):
    global json_file, exo_dir

    try:
        opts, args = getopt.getopt(argv, "ho:")
    except getopt.GetoptError as err:
        print(err)
        usage(1)
    for opt, arg in opts:
        if opt == '-h':
            usage(0)
        elif opt == "-o":
            exo_dir = arg
        else:
            assert False, "unhandled option"
    if len(args) == 0:
        print("Missing argument: <src JSON file>")
        usage(1)
    if (not exo_dir):
        print("Missing option(s): -o <dest exo dir>")
        usage(1)
    if len(args) > 1:
        print("Too many arguments:", args)
        usage(1)
    json_file = args[0]


def main(argv):
    args_parse(argv)
    print("==> Converting JSON file to exo dir...")
    print("\tSource JSON file: %s" % json_file)
    print("\tOutput exo dir:   %s" % exo_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
