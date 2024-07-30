import pymupdf
import json
import os
import tqdm

# turn off pymupdf errors
os.environ["PYMUPDF_EXCEPTIONS_VERBOSE"] = "0"

data = [json.loads(line) for line in open("computed/citing_papers-s0.jsonl")]

fout = open("computed/citing_papers-s1.jsonl", "w")

for paper in tqdm.tqdm(data):
    # in 2020 there was only one model so we can skip it
    if paper["year"] <= 2020:
        continue

    f_pdf = f"computed/fulltexts/{paper['paperId']}.pdf"
    if not os.path.isfile(f_pdf):
        continue

    try:
        doc = pymupdf.open(f_pdf)
        text_tables = "  ".join([
            table.to_markdown()
            for page in doc for table in page.find_tables().tables
        ]).lower()
        text_pdf = "  ".join([
            page.get_text() for page in doc
        ]).lower()
    except Exception:
        continue

    fout.write(
        json.dumps({
            'paperId': paper['paperId'],
            'title': paper["title"],
            'pdf': paper["pdf"],
            'text': text_pdf,
            'tables': text_tables,
        }, ensure_ascii=True) + "\n"
    )
    fout.flush()

fout.close()