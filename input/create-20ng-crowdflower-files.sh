#!/bin/sh

# convert newsgroup train data to csv
./txt2csv.py /aml/home/plf1/data/ana_datasets/ng/20ng-train-all-terms.txt > /tmp/ng.csv

# scramble instance order
head -n1 /tmp/ng.csv > /tmp/ng-shuf.csv
tail -n +2 /tmp/ng.csv | shuf >> /tmp/ng-shuf.csv

# first 1000 lines ("a") will be reannotated
head -n1001 /tmp/ng-shuf.csv > 20ng-reannotate.csv

