#!/usr/bin/python3
import re
from pprint import pprint
import json
import csv
import argparse
from os import path


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Translate values inside a json annotation stream")
    parser.add_argument('translate_from',help="The regex to match against attribute values")
    parser.add_argument('translate_to',help="The value to substitute for matched annnotation values")
    parser.add_argument('json',help="File containing JSON annotation stream" )
    parser.add_argument('-a','--attributes',nargs='+',default=["annotation"],help="The attribute to transform")
    args = parser.parse_args()

    anns = json.load(open(args.json))
    for ann in anns:
        for attribute in args.attributes:
            if attribute in ann:
                ann[attribute] = re.sub(args.translate_from, args.translate_to, ann[attribute])

    # print
    print(json.dumps(anns, separators=(',',': '), sort_keys=True, indent=4))

