import glob
import argparse
import numpy as np
import json

args = argparse.ArgumentParser()
args.add_argument("--langs", default=None)
args = args.parse_args()

data_test = [json.loads(x) for x in open("data/jsonl/test.jsonl", "r")]


for f in glob.glob("logs/*_tag*.out"):
    with open(f) as fd:
        data = fd.readlines()
    data = [float(x.strip()) for x in data]
    if args.langs is not None:
        data = [
            x for x, y in zip(data, data_test)
            if y["langs"] == args.langs
        ]
    print(f)
    print(f"{np.average(data):.3f}")