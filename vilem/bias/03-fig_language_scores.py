import matplotlib.pyplot as plt
import json
import argparse
import numpy as np
import collections

args = argparse.ArgumentParser()
args.add_argument("--langs", default=["en-de", "en-cs", "zh-en"], nargs="+")
args = args.parse_args()

_, axs = plt.subplots(3, 1, figsize=(4, 3), sharex=True)

BINS = np.linspace(0, 100, 20)

for ax, langs in zip(axs, args.langs):
    data = [json.loads(x) for x in open(f"data/jsonl/train.jsonl")]
    data = [x for x in data if x["langs"] == langs]


    ax.hist([x["score"] for x in data], bins=BINS, color="#494")
    ax.set_xlabel(f"{langs}; Score")
    ax.set_ylabel("Frequency")

    ax.set_yticks([])

    if langs == "zh-en":
        data_sys = collections.defaultdict(list)
        for line in data:
            data_sys[(line["system"], line["year"])].append(line["score"])
        data_sys = list(data_sys.values())
        # sort from lowest to highest
        data_sys.sort(key=lambda x: np.average(x))

        # take top 25% by the ordered systems, slightly more fair
        data = [x for l in data_sys for x in l]
        data = data[int(len(data)*0.75):]

        # plot highest sys
        ax.hist(data, bins=BINS, color="#b33")
        ax.text(0.8, 0.5, "remove", color="#b33", transform=ax.transAxes)
        ax.text(0.2, 0.5, "keep", color="#494", transform=ax.transAxes)


# plt.xlim(-3, 2)
plt.tight_layout(pad=0)
plt.show()