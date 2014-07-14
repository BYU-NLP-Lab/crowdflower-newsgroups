#!/bin/sh
echo "removing old json files from tmp"
rm -r tmp
mkdir tmp

# turn crowdflower annotations into an annotation stream
/usr/bin/python3 ~/git/utils/annotation_streams/crowdflower/convert.py -b /aml/data/newsgroups -o tmp/annotated.json ../results/1000/untrusted/job_505945.json 

# turn unannotated data into an "annotation" stream
/usr/bin/python3 unannotatedcsv2json.py -b /aml/data/newsgroups -o tmp/unannotated.json ../input/excluded.csv

# combine the two streams into the full annotation stream dataset
/usr/bin/python3 ~/git/utils/annotation_streams/append.py tmp/*.json > newsgroups.json

