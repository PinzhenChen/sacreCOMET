import os
import glob
import re
import json

os.makedirs("data/jsonl", exist_ok=True)

data = []

for dir in glob.glob("data/mt-metrics-eval-v2/*"):
    if os.path.isdir(dir):
        year = 2000+int(re.search(r"^wmt(\d{2})", dir.split("/")[-1]).group(1))
        print(dir)

        sources = {
            # drop last line which is empty
            f.split("/")[-1].split(".")[0]: open(f, "r").read().split("\n")[:-1]
            for f in glob.glob(f"{dir}/sources/*.txt")
        }
        documents = {
            # drop last line which is empty
            # take only the domain
            f.split("/")[-1].split(".")[0]: [line.split("\t") for line in open(f, "r").read().split("\n")[:-1]]
            for f in glob.glob(f"{dir}/documents/*.docs")
        }
        dir_short = dir.split("/")[-1]
        OVERRIDE_DOMAIN = (
            "flores" if "flores" in dir_short else
            "news" if "news" in dir_short else
            "tedtalks" if "tedtalks" in dir_short else
            None
        )
        def fix_domain(domain):
            if OVERRIDE_DOMAIN is not None:
                return OVERRIDE_DOMAIN
            if "wiki" in domain[1]:
                return "wiki"
            return (
                domain[0]
                .replace("conversation", "voice")
                .replace("speech", "voice")
                .replace("newstest2019", "news")
                .replace("newstest2020", "news")
                .replace("no-mqm", "old")
                .replace("ecommerce", "ec")
                .replace("user_review", "ec")
                .replace("ad", "ec")
                .replace("ec", "ecommerce")
                .replace("domain", "unknown")
                .replace("qa", "unknown")
            )
        documents = {
            langs: [fix_domain(domain) for domain in domains]
            for langs, domains in documents.items()
        }
        references = {
            # drop last line which is empty
            f.split("/")[-1].split(".")[0]: open(f, "r").read().split("\n")[:-1]
            for f in glob.glob(f"{dir}/references/*.txt")
        }
        targets = {
            # drop last line which is empty
            (langs, f.split("/")[-1].removesuffix(".txt")): open(f, "r").read().split("\n")[:-1]
            for langs in sources.keys()
            for f in glob.glob(f"{dir}/system-outputs/{langs}/*.txt")
        }

        for f in glob.glob(f"{dir}/human-scores/*.seg.score"):
            # skip MQM
            if ".mqm" in f:
                continue
            if "-z." in f:
                continue
            if ".psqm" in f:
                continue
            
            langs = f.split("/")[-1].split(".")[0]
            for line_i, line in enumerate(open(f, "r").read().split("\n")[:-1]):
                system, score = line.split()
                if score == "None":
                    continue
                try:
                    score = float(score)
                except ValueError:
                    continue

                # risky but works..
                line_i = line_i % len(sources[langs])

                data.append({
                    "src": sources[langs][line_i],
                    "ref": references[langs][line_i],
                    "tgt": targets[(langs, system)][line_i],
                    "score": score,
                    "year": year,
                    "langs": langs,
                    "system": system,
                    "domain": documents[langs][line_i],
                })

with open("data/jsonl/all.jsonl", "w") as f:
    f.writelines([json.dumps(line) + "\n" for line in data])

# we're removing only about 10 examples
data_train = [x for x in data if x["year"] <= 2021 if len(x["src"]+x["tgt"]+x["ref"]) < 2500]
data_test = [x for x in data if x["year"] == 2023]

print("TRAIN:", len(data_train))
print("TEST: ", len(data_test))

open("data/jsonl/train.jsonl", "w").writelines(json.dumps(line) + "\n" for line in data_train)
open("data/jsonl/test.jsonl", "w").writelines(json.dumps(line) + "\n" for line in data_test)