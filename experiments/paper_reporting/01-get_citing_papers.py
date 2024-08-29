import json
from semanticscholar import SemanticScholar
import tqdm
s2 = SemanticScholar()

COMET_PAPERS = [
    "CorpusID:221819581",
    "CorpusID:256461051",
    "CorpusID:225103036",
    "CorpusID:245856036",
    "CorpusID:252222165",
    "CorpusID:249204430",
]
# grab all papers
citing_papers = [
    paper
    for comet_paper in tqdm.tqdm(COMET_PAPERS)
    for paper in s2.get_paper(comet_paper).citations
]

print(f"Found {len(citing_papers)} citing non-unique papers")

# deduplicate
papers_out = {}
for paper in citing_papers:
    if paper.paperId not in papers_out:
        papers_out[paper.paperId] = paper

print(f"Found {len(papers_out)} citing unique papers")


with open("computed/citing_papers-s0.jsonl", "w") as f:
    f.writelines([
        json.dumps({
            "paperId": paper.paperId,
            "title": paper.title,
            "venue": paper.venue,
            "year": paper.year,
            "citationCount": paper.citationCount,
            "pdf": paper.openAccessPdf["url"],
        }) + "\n"
        for paper in papers_out.values()
        if paper.openAccessPdf
    ])