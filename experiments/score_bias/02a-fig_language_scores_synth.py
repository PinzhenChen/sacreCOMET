import matplotlib.pyplot as plt
import json
import numpy as np
import argparse
import figutils

args = argparse.ArgumentParser()
args.add_argument("--cut", default=None)
args = args.parse_args()

_, axs = plt.subplots(2, 1, figsize=(2, 3), sharex=True)

BINS = np.linspace(0, 100, 10)

for ax, langs in zip(axs, ["en-de", "en-zh"]):
    data = [json.loads(x) for x in open(f"data/jsonl/train.jsonl")]
    data = [x for x in data if x["langs"] == langs]
    data = [x["score"] for x in data]

    if langs == "en-zh":
        ax.set_xlabel("Score")
    if args.cut is None:
        ax.set_ylabel("Frequency")
    else:
        # invisible label so that dimensions remain the same
        ax.set_ylabel("Frequency", color="white")

    ax.set_yticks([])
    # scale by the original data
    ax.set_ylim(0, max(np.histogram(data, bins=BINS)[0])*1.1)

    ax.text(
        0.1, 0.5,
        r"$\rightarrow$".join([x.capitalize() for x in langs.split("-")]),
        color="black",
        transform=ax.transAxes,
        size=13
    )

    if langs == "en-zh" and args.cut is not None:
        data.sort()
        if args.cut == "top":
            data = data[int(len(data)*0.25):]
        elif args.cut == "bot":
            data = data[:int(len(data)*0.75)]
        else:
            raise Exception("Invalid cut " + args.cut)
        

        ax.text(
            0.1, 0.35,
            args.cut.replace("bot", "bottom").capitalize() + r" 75%",
            color="black",
            transform=ax.transAxes,
            size=9
        )


    ax.hist(data, bins=BINS, color="#444")

    ax.spines[['top', 'right']].set_visible(False)

    # data_sys = collections.defaultdict(list)
    # for line in data:
    #     data_sys[(line["system"], line["year"])].append(line["score"])
    # data_sys = list(data_sys.values())
    # # sort from lowest to highest
    # data_sys.sort(key=lambda x: np.average(x))

plt.tight_layout(pad=0)
plt.savefig(f"computed/fig_bias_setup_{'0' if args.cut is None else '1'}.pdf")
plt.show()