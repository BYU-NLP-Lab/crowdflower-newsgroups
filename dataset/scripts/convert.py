#!/usr/bin/python3
import jsonmess
import calendar
from dateutil import parser as dateparser
import argparse
import os
import json

def timestamp(str):
    dt = dateparser.parse(str)
    return calendar.timegm(dt.timetuple())

def custom_objects_from_crowdflower(basedir,jsonpath,min_trust,min_worker_trust):
    """ crowdflower json files return a newline-separated 
    list of json objects, which is not technically correct json"""
    for job in jsonmess.load(jsonpath):
        for judge in job["results"]["judgments"]:
            index = judge["unit_data"]["index"]
            label = judge["unit_data"]["hidden_label"]
            golden = bool(judge["unit_data"]["_golden"])
            trust = judge["trust"] or 0
            worker_trust = judge["worker_trust"] or 0
            #hidden_label = judge["unit_data"]["hidden_label"] # gold for all units

            if trust>=min_trust and worker_trust>=min_worker_trust:
                # we allowed a set of up to three categories to be selected for each judgment. 
                # cycle through all of them.
                for cat in judge["data"]["category"]:
                    yield {   
                        # "batch": None, # we didn't get batch infor from crowdflower that I can see
                        "source": index,
                        "datapath": os.path.join(basedir,index),
                        "label": label,
                        "labelObserved": golden,
                        "annotator": judge["worker_id"],
                        "annotation": cat,
                        "startTime": timestamp(judge["started_at"]),
                        "endTime": timestamp(judge["created_at"])
                    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infiles",nargs="+",help="One or more crowdflower json files to be converted.")
    parser.add_argument("--outfile",'-o',help="Output annotation stream file.")
    parser.add_argument("--basedir",'-b',default="/aml/data/newsgroups",help="Output annotation stream file.")
    parser.add_argument("--min-trust",type=float,default=0.0,help="Filter out all judgments which crowdflower gave a 'trust' lower than this.")
    parser.add_argument("--min-worker-trust",type=float,default=0.0,help="Filter out all judgments make by a worker whose crowdflower 'trust' is lower than this.")
    args = parser.parse_args()

    outfile = open(args.outfile,'w')
    outfile.write('[\n')
    for infile in args.infiles:
        for i,obj in enumerate(custom_objects_from_crowdflower(args.basedir,infile,args.min_trust,args.min_worker_trust)):
            if i>0:
                outfile.write(",\n")
            json.dump(obj,outfile)
    outfile.write('\n]')
    outfile.close()
