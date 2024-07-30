import json
import random

data = [json.loads(x) for x in open("data/jsonl/train.jsonl", "r")]

random.seed(0)

for line in data:
    if random.choice([True, False]):
        line["ref"], line["src"] = line["src"], line["ref"]

with open(f"data/jsonl/train.swap50.jsonl", "w") as f:
    f.writelines([json.dumps(line) + "\n" for line in data])
