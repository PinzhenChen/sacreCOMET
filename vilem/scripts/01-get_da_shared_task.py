# !wget https://storage.googleapis.com/mt-metrics-eval/mt-metrics-eval-v2.tgz

import os
import glob
import re
import json

data = []

for dir in glob.glob("data/mt-metrics-eval-v2/*"):
    if os.path.isdir(dir):
        year = 2000+int(re.search(r"^wmt(\d{2})", dir.split("/")[-1]).group(1))
        print(year)

        sources = {
            # drop last line which is empty
            f.split("/")[-1].split(".")[0]: open(f, "r").read().split("\n")[:-1]
            for f in glob.glob(f"{dir}/sources/*.txt")
        }
        references = {
            # drop last line which is empty
            f.split("/")[-1].split(".")[0]: open(f, "r").read().split("\n")[:-1]
            for f in glob.glob(f"{dir}/references/*.txt")
        }
        targets = {
            # drop last line which is empty
            (lang, f.split("/")[-1].removesuffix(".txt")): open(f, "r").read().split("\n")[:-1]
            for lang in sources.keys()
            for f in glob.glob(f"{dir}/system-outputs/{lang}/*.txt")
        }

        for f in glob.glob(f"{dir}/human-scores/*.seg.score"):
            lang = f.split("/")[-1].split(".")[0]
            for line_i, line in enumerate(open(f, "r").read().split("\n")[:-1]):
                system, score = line.split()
                if score == "None":
                    continue
                try:
                    score = float(score)
                except ValueError:
                    continue

                # risky but works..
                line_i = line_i % len(sources[lang])

                data.append({
                    "src": sources[lang][line_i],
                    "ref": references[lang][line_i],
                    "tgt": targets[(lang, system)][line_i],
                    "score": score,
                    "year": year,
                })

with open("data/mt-metrics-eval-v2.jsonl", "w") as f:
    f.writelines([json.dumps(line) + "\n" for line in data])