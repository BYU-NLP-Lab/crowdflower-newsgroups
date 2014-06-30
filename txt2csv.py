#!/usr/bin/python
import argparse

def linesof(paths):
    for path in paths:
        for line in open(path):
            yield line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform text files where each line represents a document and the first word is the true category into a csv fild suitable for use with crowdflower.")
    parser.add_argument("infiles",nargs="+",help="A text file where each line represents a document and the first word is the true document category")
    args = parser.parse_args()

    # header
    print ",".join(["index","category_gold","document"])

    # body
    idx=0
    for line in linesof(args.infiles):
        label,sentence = line.strip().split("\t")
        print ",".join([str(idx), label, sentence])
        idx += 1
        
