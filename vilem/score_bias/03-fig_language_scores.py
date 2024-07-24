import matplotlib.pyplot as plt
import json
import argparse
import numpy as np

args = argparse.ArgumentParser()
args.add_argument("--langs", default=["en-de", "en-cs", "zh-en"], nargs="+")
args = args.parse_args()

_, axs = plt.subplots(3, 1, figsize=(4, 3), sharex=True)

BINS = np.arange(-3, 2, 0.1)

for ax, langs in zip(axs, args.langs):
    data = [json.loads(x) for x in open(f"data/da/general/{langs}.jsonl")]
    data = [x["score"] for x in data]

    ax.hist(data, bins=BINS, color="#494")
    ax.set_xlabel(f"{langs}; Score")
    ax.set_ylabel("Frequency")

    ax.set_yticks([])

    if langs == "zh-en":
        data = [x for x in data if x > 0.5]
        ax.hist(data, bins=BINS, color="#b33")
        ax.text(0.8, 0.5, "remove", color="#b33", transform=ax.transAxes)
        ax.text(0.2, 0.5, "keep", color="#494", transform=ax.transAxes)


plt.xlim(-3, 2)
plt.tight_layout(pad=0)
plt.show()