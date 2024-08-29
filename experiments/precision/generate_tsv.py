import csv
import json

import sys
import glob
import os

"""
Split the .jsonl file into .tsv files by [Attribute]
"""

dataDir = "/mnt/startiger0/tlam/proj/testingCOMET/testingCOMET/vilem/data/jsonl/test.jsonl"
attr = 'langs' #e.g. langs

data_by_attr = {}
#sorting
with open(dataDir, "r") as json_file:
    for idx, l in enumerate(json_file):
        line = json.loads(l)
        if idx == 0:
            HEADER = list(line.keys())
        else:
            assert HEADER == list(line.keys())

        langs = line[attr]

        if langs not in data_by_attr:
            data_by_attr[langs] = [line]
        else:
            data_by_attr[langs].append(line)

#output
for attr in list(data_by_attr.keys()):
    outFile = f"output.{attr}.tsv"
    with open(outFile, "w") as fo:
        writer = csv.DictWriter(fo, HEADER, delimiter="\t")
        writer.writeheader()
        writer.writerows(data_by_attr[attr])

