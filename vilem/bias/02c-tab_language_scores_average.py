import json
import numpy as np

data = [json.loads(x) for x in open(f"data/jsonl/train.jsonl")]

LANGS = list({x["langs"] for x in data})
LANGS.sort(key=lambda x: 2*x.startswith("en-")+1*x.endswith("-en"))

for langs in LANGS:
    data_local = [x["score"] for x in data if x["langs"] == langs]
    langs = r"$\rightarrow$".join([x.capitalize() for x in langs.split("-")])
    print(
        f"{langs} & {np.average(data_local):.2f}",
        end=r" \\" + "\n"
    )