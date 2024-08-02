import collections
import json
import numpy as np

data = [json.loads(x) for x in open("data/jsonl/train.jsonl", "r")]

def maim_language(data, langs):
    data_rest = [line for line in data if line["langs"] != langs]
    data = [line for line in data if line["langs"] == langs]

    # MODE 1 "flat": just top 25% of the scores
    data = sorted(data, key=lambda x: x["score"])
    data_lang_top = data[int(len(data)*0.25):]
    data_lang_bot = data[:int(len(data)*0.75)]

    with open(f"data/jsonl/train.{langs}.top-flat.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_lang_top+data_rest])

    with open(f"data/jsonl/train.{langs}.bot-flat.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_lang_bot+data_rest])

    # MODE 2 "sys": top 25% of the scores by the system
    data_sys = collections.defaultdict(list)
    for line in data:
        data_sys[(line["system"], line["year"])].append(line)
    data_sys = list(data_sys.values())
    # sort from lowest to highest
    data_sys.sort(key=lambda x: np.average([line["score"] for line in x]))

    # take top/bot 75% by the ordered systems, slightly more fair
    data = [x for l in data_sys for x in l]
    data_lang_top = data[int(len(data)*0.25):]
    data_lang_bot = data[:int(len(data)*0.75)]

    with open(f"data/jsonl/train.{langs}.top-sys.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_lang_top+data_rest])

    with open(f"data/jsonl/train.{langs}.bot-sys.jsonl", "w") as f:
        f.writelines([json.dumps(line) + "\n" for line in data_lang_bot+data_rest])

maim_language(data, "en-de")
maim_language(data, "en-zh")

