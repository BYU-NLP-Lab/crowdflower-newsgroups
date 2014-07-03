#!/usr/bin/python
from random import shuffle
from collections import Counter
import argparse
import csv

goldcol = "category_gold"
goldreasoncol = "category_gold_reason"
goldreasonval = "The author of this text originally posted it under the indicated category."
hiddencol = "hidden_label"
testcol = "_golden" # required by crowdflower to indicate 

def get_categories(data):
    classes = set()
    for row in data:
        classes.add(row[goldcol])
    return classes
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a csv file into two--one to be included in the crowdflower study, and one to be excluded. The included csv will include a certain number of instances, and also a certain number of instances with trusted labels (in the category_gold column). All instances not chosen to have a trusted label will preserve the true label in the 'hidden_label' column.")
    parser.add_argument("--infile",default="all.csv",help="The input csv (must have col named 'category_gold' containing true instacne labels).")
    parser.add_argument("--included",default="included.csv",help="The name of the included instances.")
    parser.add_argument("--excluded",default="excluded.csv",help="The name of the excluded instances.")
    parser.add_argument("--num-to-include",type=int,default=1000,help="The number of instances to include")
    parser.add_argument("--num-trusted-labels-per-class",type=int,default=10,help="The number of trusted labels per class.")
    args = parser.parse_args()

    # read big csv
    reader = csv.DictReader(open(args.infile))
    fieldnames = reader.fieldnames[:]
    if hiddencol not in fieldnames:
        fieldnames.append(hiddencol)
    if goldreasoncol not in fieldnames:
        fieldnames.append(goldreasoncol)
    if testcol not in fieldnames:
        fieldnames.append(testcol)
    data = [d for d in reader]
    shuffle(data)

    # prepare to write two smaller csvs
    inc_file = open(args.included,'w')
    inc_writer = csv.DictWriter(inc_file,fieldnames)
    inc_writer.writeheader()
    exc_file = open(args.excluded,'w')
    exc_writer = csv.DictWriter(exc_file,fieldnames)
    exc_writer.writeheader()

    # get the categories
    categories = get_categories(data)
    n = args.num_trusted_labels_per_class

    trusted_cnt = Counter()
    included_cnt = 0
    for row in data:
        row[goldreasoncol] = goldreasonval
        # copy gold label into hidden column
        if hiddencol not in row:
            row[hiddencol] = row[goldcol]
        # choose n trusted labels per category
        cat = row[hiddencol]
        if trusted_cnt[cat] < n:
            row[goldcol] = row[hiddencol] # ensure gold column is not hidden
            row[testcol] = "TRUE"
            inc_writer.writerow(row)
            trusted_cnt[cat] += 1
        # choose n 
        elif included_cnt < args.num_to_include:
            row[goldcol] = "" # hide gold column
            row[testcol] = "FALSE"
            inc_writer.writerow(row)
            included_cnt += 1
        else:
            row[goldcol] = "" # hide gold column
            exc_writer.writerow(row)

    inc_file.close()
    exc_file.close()

    # sanity check
    if min(trusted_cnt.values()) < n:
        raise Exception("Unable to find %d instances for each category: %s" % (n,trusted_cnt))
    if included_cnt != args.num_to_include:
        raise Exception("Unable to find %d instances to include" % args.num_to_include)

