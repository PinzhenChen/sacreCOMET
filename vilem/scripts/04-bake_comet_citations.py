import requests
import json

def get_citation(url):
    if "arxiv" in url:
        return requests.get(f"https://arxiv.org/bibtex/{url.split('/')[-1]}").text
    if "anthology" in url:
        return requests.get(f"https://aclanthology.org/{url.split('/')[-1]}.bib").text


# should not be a direct pdf and should not end with /
MODELS = {
    "Unbabel/wmt23-cometkiwi-da-xl-marian": "Unbabel/wmt22-cometkiwi-da",
    "Unbabel/wmt21-comet-qe-mqm-marian": "https://aclanthology.org/2021.findings-emnlp.330",
    "Unbabel/wmt21-comet-qe-da-marian": "https://aclanthology.org/2021.findings-emnlp.330",
    "Unbabel/wmt21-comet-da-marian": "https://aclanthology.org/2021.findings-emnlp.330",
    "Unbabel/wmt20-comet-qe-da-v2-marian": "Unbabel/wmt20-comet-qe-da",
    "Unbabel/wmt20-comet-qe-da-marian": "Unbabel/wmt20-comet-qe-da",
    "Unbabel/wmt20-comet-da-marian": "Unbabel/wmt20-comet-da",
    "Unbabel/wmt22-comet-da-marian": "Unbabel/wmt22-comet-da",
    "Unbabel/wmt23-cometkiwi-da-xxl-marian": "Unbabel/wmt23-cometkiwi-da-xxl",
    "Unbabel/wmt22-cometkiwi-da-marian": "Unbabel/wmt22-cometkiwi-da",

    "Unbabel/WMT24-QE-task2-baseline": "https://aclanthology.org/2022.wmt-1.60",
    "Unbabel/wmt22-cometkiwi-da": "https://aclanthology.org/2022.wmt-1.60",
    "Unbabel/XCOMET-XL": "https://arxiv.org/abs/2310.10482",
    "Unbabel/XCOMET-XXL": "https://arxiv.org/abs/2310.10482",
    "Unbabel/TowerInstruct-13B-v0.1": "https://arxiv.org/abs/2402.17733",
    "Unbabel/TowerInstruct-7B-v0.2": "https://arxiv.org/abs/2402.17733",
    "Unbabel/TowerBase-7B-v0.1": "https://arxiv.org/abs/2402.17733",
    "Unbabel/TowerBase-13B-v0.1": "https://arxiv.org/abs/2402.17733",
    "Unbabel/TowerInstruct-7B-v0.1": "https://arxiv.org/abs/2402.17733",
    "Unbabel/unite-xl": "https://aclanthology.org/2022.acl-long.558",
    "Unbabel/unite-xxl": "https://aclanthology.org/2022.acl-long.558",
    "Unbabel/unite-mup": "https://aclanthology.org/2022.acl-long.558",
    "Unbabel/wmt22-cometkiwi-da": "https://aclanthology.org/2022.wmt-1.60",
    "Unbabel/wmt23-cometkiwi-da-xl": "https://arxiv.org/abs/2309.11925",
    "Unbabel/wmt23-cometkiwi-da-xxl": "https://arxiv.org/abs/2309.11925",
    "Unbabel/wmt22-unite-da": "https://arxiv.org/abs/2305.11806",

    "Unbabel/eamt22-cometinho-da": "https://aclanthology.org/2022.eamt-1.9",
    "Unbabel/wmt20-comet-da": "https://aclanthology.org/2020.wmt-1.101",
    "Unbabel/wmt20-comet-qe-da": "https://aclanthology.org/2020.wmt-1.101",
    "Unbabel/wmt22-comet-da": "https://aclanthology.org/2022.wmt-1.52",

    "default": "https://aclanthology.org/2020.emnlp-main.21",
}

MODELS_OUT = {}

for name, tgt in MODELS.items():
    # for marian redirects
    if tgt in MODELS.keys():
        tgt = MODELS[tgt]

    citation = get_citation(tgt)
    MODELS_OUT[name.lower()] = {
        "url": tgt,
        "citation": citation
    }

with open("python-tool/papers.json", "w") as f:
    json.dump(MODELS_OUT, f, indent=2)