#!/usr/bin/python
import txt2image
import argparse
import glob
import os
from os import path
from subprocess import call
import csv

def n_lines(n,text):
    lines,head = 0,0
    while lines<n:
        head += text.index('\n')
        lines += 1
    return text[:head]

def filter_ng_header(text):
    sections = text.split("\n\n")
    header = sections[0]
    body = "\n\n".join(sections[1:])
    # remove all header lines except for the subject line
    subject_line = [line for line in header.split("\n") if "Subject:" in line[0:8]]
    if len(subject_line)!=1:
        raise Exception("header must contain only a single header line: %s" % header)
    return "\n\n".join([subject_line[0],body])

def text_path_generator(basedir,outdir,csvfile,max_doc_lines):
    for row in csv.DictReader(open(csvfile)):
        docpath = path.join(basedir,row['index'])
        short_doc = path.join(outdir,row['short_doc'])
        full_doc = path.join(outdir,row['full_doc'])

        # read doc text and filter non-subject headers
        text = open(docpath).read()
        filtered_text = filter_ng_header(text)

        # short doc
        yield n_lines(args.max_doc_lines,filtered_text), short_doc

        # full doc
        fullpath = path.join(full_doc,"full_doc")
        yield (filtered_text, fullpath)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a human readable .png version of the indicated newsgroups documents. 1) all header lines have been stripped except for the messages subject, 2) all docs have a short and long version")
    parser.add_argument("--basedir",default="/aml/data/newsgroups",help="The directory where the newsgroups corpus lives, organized in a file/folder hierarchy where files such as newsgroups/indices/dataset/split/category0.txt contain relative file paths for a document with the label category0.")
    parser.add_argument("--csvfile",default="included.csv",help="The name of the csv file whose instances should be converted. There must be a column named 'index' which points to the relative path of each instance, 'short_doc', and 'full_doc' which point to locations for a file/folder to be written, respectively.")
    parser.add_argument("--outdir",default="/aml/home/plf1/public_html/newsgroups",help="The location of the output directory")
    parser.add_argument("--max-doc-lines",type=int,default=25,help="The max number of lines the short doc summary has in it.")
    args = parser.parse_args()

    # write images
    txt2image.write_images_in_parallel(text_path_generator(
        args.basedir,
        args.outdir,
        args.csvfile,
        args.max_doc_lines))

