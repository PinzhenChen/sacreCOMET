raise Exception("Deprecated")

#!/usr/bin/env python3

#
# Downloads publicly available DA data which are already zscored.
#

from datasets import load_dataset
import os
import csv
import json

os.makedirs(f"data/da/general", exist_ok=True)

dataset = load_dataset("RicardoRei/wmt-da-human-evaluation")
data_all = []
open_files = {}


def get_file(langs):
    if langs not in open_files:
        open_files[langs] = open(
            f"data/da/general/{langs}.jsonl",
            "w"
        )
    return open_files[langs]


for line in dataset["train"]:
    line_new = {
        "src": line["src"],
        "tgt": line["mt"],
        "ref": line["ref"],
        "score": line["score"],
        "domain": line["domain"],
        "year": line["year"],
        "langs": line["lp"],
    }
    data_all.append(line_new)
    get_file(line['lp']).write(json.dumps(line_new, ensure_ascii=False) + "\n")

data_train = []
data_test = []

for line in data_all:
    if line["year"] >= 2022:
        data_test.append(line)
    else:
        data_train.append(line)

# create base CSV files for training
with open(f"data/da/general/train.csv", "w") as f:
    f.write("lp,src,mt,ref,score,system,annotators,domain\n")
    f = csv.writer(f)
    f.writerows([
        (
            line["langs"], line["src"], line["tgt"],
            line["ref"], line["score"], "", "", line["domain"],
        )
        for line in data_train
    ])
with open(f"data/da/general/test.csv", "w") as f:
    f.write("lp,src,mt,ref,score,system,annotators,domain\n")
    f = csv.writer(f)
    f.writerows([
        (
            line["langs"], line["src"], line["tgt"],
            line["ref"], line["score"], "", "", line["domain"],
        )
        for line in data_test
    ])