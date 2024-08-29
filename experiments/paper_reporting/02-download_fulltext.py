import os
import urllib.request
import json

os.makedirs("computed/fulltexts", exist_ok=True)

data = [json.loads(line) for line in open("computed/citing_papers-s0.jsonl")]

for paper in data:
    try:
        urllib.request.urlretrieve(paper["pdf"], f"computed/fulltexts/{paper['paperId']}.pdf")
    except Exception as e:
        print("Failed", e)
        print("Continuing...")