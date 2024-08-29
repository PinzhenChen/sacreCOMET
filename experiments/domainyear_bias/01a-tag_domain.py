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
        data_agg[line["domain"]].append(line["score"])

    for domain, scores in data_agg.items():
        print(f"{domain:>15} {len(scores):>6}: {np.average(scores):.2f}")

data = [json.loads(x) for x in open(f"data/jsonl/train.jsonl", "r")]
data = [
    {
        **line,
        "tgt": f'{line["domain"]} {line["tgt"]}',
    }
    for line in data
]

with open(f"data/jsonl/train.tagdomain.jsonl", "w") as f:
    f.writelines([json.dumps(line) + "\n" for line in data])

data = [json.loads(x) for x in open(f"data/jsonl/test.jsonl", "r")]
for domain in tqdm.tqdm(["flores", "news", "wiki"]):
    data_local = copy.deepcopy(data)
    data_local = [
        {
            **line,
            "tgt": f'{domain} {line["tgt"]}',
        }
        for line in data_local
    ]

    with open(f"data/jsonl/test.tagdomain.{domain}.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_local])
