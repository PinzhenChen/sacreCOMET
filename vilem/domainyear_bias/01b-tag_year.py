import json
import collections
import numpy as np
import copy

import tqdm

for data in ["train", "test"]:
    print(data)
    data = [json.loads(x) for x in open(f"data/jsonl/{data}.jsonl", "r")]
    data_agg = collections.defaultdict(list)

    for line in data:
        data_agg[line["year"]].append(line["score"])

    for year, scores in data_agg.items():
        print(f"{year:>5} {len(scores):>6}: {np.average(scores):.2f}")


data = [json.loads(x) for x in open(f"data/jsonl/train.jsonl", "r")]
data = [
    {
        **line,
        "tgt": f'{line["year"]} {line["tgt"]}',
    }
    for line in data
]

with open(f"data/jsonl/train.tagyear.jsonl", "w") as f:
    f.writelines([json.dumps(line) + "\n" for line in data])


data = [json.loads(x) for x in open(f"data/jsonl/test.jsonl", "r")]
for year in tqdm.tqdm(["2019", "2020", "2021", "2022", "2023", "2024", "2025"]):
    data_local = copy.deepcopy(data)
    data_local = [
        {
            **line,
            "tgt": f'{line["year"]} {line["tgt"]}',
        }
        for line in data_local
    ]

    with open(f"data/jsonl/test.tagyear.{year}.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_local])
