#!/usr/bin/python
import txt2image
import argparse
import glob
import os
from os import path
from subprocess import call

def filter_ng_header(text):
    sections = text.split("\n\n")
    header = sections[0]
    body = "\n\n".join(sections[1:])
    # remove all header lines except for the subject line
    subject_line = [line for line in header.split("\n") if "Subject:" in line[0:8]]
    if len(subject_line)!=1:
        raise Exception("header must contain only a single header line: %s" % header)
    return "\n\n".join([subject_line[0],body])

def iterate_dataset(basedir,dataset,split):
    for indexfile in glob.glob("%s/*" % path.join(basedir,"indices",dataset,split)):
        # get the category from the filename (e.g., alt.atheism.txt)
        category = path.splitext(path.basename(indexfile))[0]
        for docpath in open(indexfile):
            yield category,docpath.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a version of newsgroups in which all header lines have been stripped except for the messages subject.")
    parser.add_argument("--basedir",default="/aml/data/newsgroups",help="The directory where the newsgroups corpus lives, organized in a file/folder hierarchy where files such as newsgroups/indices/dataset/split/category0.txt contain relative file paths for a document with the label category0.")
    parser.add_argument("--dataset",default="full_set",help="The name of the dataset to convert.")
    parser.add_argument("--split",default="all",help="The name of the split to convert.")
    parser.add_argument("--outdir",default="/aml/home/plf1/public_html/newsgroups",help="The location of the output directory")
    args = parser.parse_args()

    # copy each indexed document to the new location, processing headers along the way
    for category,docpath in iterate_dataset(args.basedir,args.dataset,args.split):
        # read doc text and filter non-subject headers
        text = open(path.join(args.basedir,docpath)).read()
        filtered_text = filter_ng_header(text)
        # strip path which gives away true label
        docname = path.basename(docpath)
        abs_docpath = path.join(args.outdir,docname)
        # write filtered text to file, ensuring folder exists first
        try:
            os.makedirs(path.dirname(abs_docpath))
        except OSError:
            pass
        
        txt2image.write_image(filtered_text,abs_docpath)
        #f=open(abs_docpath,'w')
        #f.write(filtered_text)
        #f.close()
        

