import json
import glob
import numpy as np

LANGS = ["en-de", "en-zh"]

for f in glob.glob("data/jsonl/train.jsonl") + glob.glob("data/jsonl/train.*.top-*.jsonl") + glob.glob("data/jsonl/train.*.bot-*.jsonl"):
    data = [json.loads(x) for x in open(f, "r")]
    f = f.split("/")[-1].removesuffix(".jsonl").removeprefix("train.").replace("train", "original")
    print(
        f'{f:>20}',
        f'{len(data)//1000}k',
        f'{LANGS[0]} {np.average([x["score"] for x in data if x["langs"] == LANGS[0]]):.1f}',
        f'{LANGS[1]} {np.average([x["score"] for x in data if x["langs"] == LANGS[1]]):.1f}',
        sep=" | ",
    )