import json
import re
import tqdm

RE_COMET_MODEL = re.compile(r"(comet[ \-](da|20|21|22|23)|wmt(20|21|22|23)\-comet|xcomet\-|wmt\-da\-estimator)")

data = [json.loads(line) for line in open("computed/citing_papers-s1.jsonl")]

fout = open("computed/citing_papers-s2.jsonl", "w")

for paper in tqdm.tqdm(data):
    uses_comet = "comet" in paper["tables"].lower()
    reports_comet = RE_COMET_MODEL.search(paper["text"]) is not None

    if uses_comet and not reports_comet:
        fout.write(
            json.dumps({
                'paperId': paper['paperId'],
                'title': paper["title"],
                'pdf': paper["pdf"],
            }, ensure_ascii=False) + "\n"
        )
        fout.flush()


fout.close()