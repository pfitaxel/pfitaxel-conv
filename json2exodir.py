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
import re
from subprocess import check_call
import sys

version = "0.2.2"

routing = [
    ("prelude", "prelude.ml"),
    ("solution", "solution.ml"),
    ("question", "descr.md"),
    ("prepare", "prepare.ml"),
    ("template", "template.ml"),
]

test_routing = ("test", "testml", "test.ml")

test_ignore = [
    "testhaut",
]

meta_routing = ("metadata", "meta.json")

metadata_routing_v1 = [
    ("titre", "title"),
    ("diff", "stars"),
    ("description", "short_description"),
]

metadata_append_v1 = {
    "learnocaml_version": "1",
    "kind": "exercise",
}

metadata_ignore_v1 = [
    "id",
]

routing_ignore = [
    "mtime",
    "incipit",
    "checkbox",
]


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
    if not exo_dir:
        print("Missing option(s): -o <dest exo dir>")
        usage(1)
    if len(args) == 0:
        print("Missing argument: <src JSON file>")
        usage(1)
    if len(args) > 1:
        print("Too many arguments:", args)
        usage(1)
    json_file = args[0]


def write_element_to_file(basename, contents):
    if not exo_dir:
        print("Error: exo_dir variable is not set.")
        exit(2)
    filename = re.sub(r'/?$', '/' + basename, exo_dir)
    print("==> Writing contents to %s" % filename)
    with open(filename, 'w') as f:
        f.write(contents)


def ignore_fields(obj, fields):
    for field in fields:
        obj.pop(field, None)


def dump_keys(obj):
    for key, val in obj.items():
        print(key)


def echo(cmd):
    # TODO: Add quotes?
    print('$', end=' ')
    for a in cmd:
        print(a, end=' ')
    print(flush=True)


def main(argv):
    args_parse(argv)

    print("==> Converting JSON file to exo dir...")
    print("\tSource JSON file: %s" % json_file)
    print("\tOutput exo dir:   %s" % exo_dir)

    cmd = ["mkdir", "-v", "-p", "--", exo_dir]
    echo(cmd)
    check_call(cmd)

    with open(json_file) as json_data:
        json_dict = json.load(json_data)

    # dump_keys(json_dict)

    # Process the metadata fields
    meta_src = json_dict.pop(meta_routing[0])
    meta_dest = metadata_append_v1
    for srckey, destkey in metadata_routing_v1:
        strval = meta_src.pop(srckey)
        meta_dest[destkey] = strval
    ignore_fields(meta_src, metadata_ignore_v1)
    if meta_src:
        print("Warning: unconverted metadata subfields:")
        dump_keys(meta_src)
    meta_dest_json = json.dumps(meta_dest, sort_keys=True, indent=4)
    write_element_to_file(meta_routing[1], meta_dest_json)

    # Process the test code
    test_dict = json_dict.pop(test_routing[0])
    test_ml = test_dict.pop(test_routing[1])
    ignore_fields(test_dict, test_ignore)
    if test_dict:
        print("Warning: unconverted test subfields:")
        dump_keys(meta_src)
    write_element_to_file(test_routing[2], test_ml)

    # Process the OCaml fields
    for srckey, destfile in routing:
        strval = json_dict.pop(srckey)
        write_element_to_file(destfile, strval)
    ignore_fields(json_dict, routing_ignore)
    if json_dict:
        print("Warning: unconverted fields:")
        dump_keys(json_dict)


if __name__ == "__main__":
    main(sys.argv[1:])
