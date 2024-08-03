raise Exception("This doesn't work as exppected..")

from huggingface_hub import HfApi, ModelFilter, hf_hub_download
import re

RE_GET_URL = re.compile(r"\((https://[^\)]+)\)")

hf_models = list(HfApi().list_models(
    filter=ModelFilter(author="Unbabel")
))


for model in hf_models:
    if model.author != "Unbabel":
        continue
    
    print(model.id)
    try:
        with open(hf_hub_download(repo_id=model.id, filename="README.md")) as f:
            readme = f.read()
    except:
        print(f"Failed to download")
        continue

    matches = RE_GET_URL.search(readme)
    if not matches:
        continue
    for url in matches.groups():
        if "huggingface" in url:
            continue
        if "github" in url:
            continue
        print("URL: ", url)