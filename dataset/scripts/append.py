#!/usr/bin/python3
from pprint import pprint
import json
import csv
import argparse
from os import path
import sys


def sortkey(ann):
    '''sort by annotation endTime (and secondarily by AssignmentId)'''
    batch = ann['batch'] if 'batch' in ann else sys.maxsize
    endtime = ann['endTime'] if 'endTime' in ann else sys.maxsize
    return (endtime,batch)

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Combines two json annotation streams, ordering by endTime + batch")

    parser.add_argument('json',nargs='+',help="Files containing JSON annotation streams" )
    args = parser.parse_args()

    # aggregate annotations
    anns = []
    for jsonfile in args.json:
        anns.extend(json.load(open(jsonfile,errors='ignore')))

    # sort
    anns.sort(key=sortkey)

    # print
    print(json.dumps(anns, separators=(',',': '), sort_keys=True, indent=4))

