import json
import collections
import numpy as np

for data in ["train", "test"]:
    print(data)
    data = [json.loads(x) for x in open(f"data/jsonl/{data}.jsonl", "r")]
    data_agg = collections.defaultdict(list)

    for line in data:
        data_agg[line["year"]].append(line["score"])

    for year, scores in data_agg.items():
        print(f"{year:>5} {len(scores):>6}: {np.average(scores):.2f}")