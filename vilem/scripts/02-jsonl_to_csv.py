import json
import csv
import glob
import os

os.makedirs("data/csv", exist_ok=True)
os.makedirs("data/jsonl", exist_ok=True)

for f in glob.glob("data/jsonl/*.jsonl"):
    print("Check", f, end=" ")
    f = f.split("/")[-1].removesuffix(".jsonl")
    if os.path.exists(f"data/csv/{f}.csv"):
        if len(open(f"data/csv/{f}.csv", "r").readlines()) != len(open(f"data/jsonl/{f}.jsonl", "r").readlines()) + 1:
            print("- exists in CSV but different length, processing")
        else:
            print("- exists in CSV in the same length, skipping")
            continue
    else:
        print("- does not exist in CSV, processing")
    
    data = [json.loads(x) for x in open(f"data/jsonl/{f}.jsonl", "r")]
    with open(f"data/csv/{f}.csv", "w") as f:
        f.write("lp,src,mt,ref,score,system,annotators,domain\n")
        f = csv.writer(f)
        f.writerows([
            (
                line["langs"], line["src"], line["tgt"],
                line["ref"], line["score"], "", "", "no-domain",
            )
            for line in data
        ])