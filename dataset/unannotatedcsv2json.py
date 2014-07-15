#!/usr/bin/python
import argparse
import os
import json
import csv


def custom_objects_from_csv(basedir,csvpath):
    reader = csv.DictReader(open(csvpath))
    for item in reader:
        index = item["index"]
        label = item["hidden_label"]
        yield {   
            # no batch
            # no annotator/anntoations/startTime/endTime
            "label": label,
            "source": index,
            "datapath": os.path.join(basedir,index),
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infiles",nargs="+",help="One or more csv files like 'excluded.csv'.")
    parser.add_argument("--outfile",'-o',help="Output annotation stream file.")
    parser.add_argument("--basedir",'-b',default="/aml/data/newsgroups",help="Output annotation stream file.")
    args = parser.parse_args()

    outfile = open(args.outfile,'w')
    outfile.write('[\n')
    for infile in args.infiles:
        for i,obj in enumerate(custom_objects_from_csv(args.basedir,infile)):
            if i>0:
                outfile.write(",\n")
            json.dump(obj,outfile)
    outfile.write(']')
    outfile.close()
