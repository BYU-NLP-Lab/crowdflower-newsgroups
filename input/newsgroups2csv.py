#!/usr/bin/python
import argparse
import glob
from os import path
from uuid import uuid4

def iterate_dataset(basedir,dataset,split):
    for indexfile in glob.glob("%s/*" % path.join(basedir,"indices",dataset,split)):
        # get the category from the filename (e.g., alt.atheism.txt)
        category = path.splitext(path.basename(indexfile))[0]
        for docpath in open(indexfile):
            yield category, docpath.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform text files where each line represents a document and the first word is the true category into a csv fild suitable for use with crowdflower.")
    parser.add_argument("--basedir",default="/aml/data/newsgroups",help="The directory where the newsgroups corpus lives, organized in a file/folder hierarchy where files such as newsgroups/indices/dataset/split/category0.txt contain relative file paths for a document with the label category0.")
    parser.add_argument("--dataset",default="full_set",help="The name of the dataset to convert.")
    parser.add_argument("--split",default="all",help="The name of the split to convert.")
    args = parser.parse_args()

    # header
    print ",".join(["index","short_doc","full_doc","category_gold"])

    # body
    used_uuids = set()
    categories = []
    for category,index in iterate_dataset(args.basedir,args.dataset,args.split):
        # obfuscate
        obfuscated = str(uuid4())
        while obfuscated in used_uuids:
            obfuscated = str(uuid4())
        shortdoc = "%s.png" % obfuscated
        fulldoc = "%s-full" % obfuscated
        print ",".join([index,shortdoc,fulldoc,category])

