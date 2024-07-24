# for each language remove separatedly lowest and highest system
# we don't have access to systems, so let's just pop the highest and lowest segments for each source

import json
import glob
from copy import deepcopy

data = []
for f in glob.glob("data/da/general/*-*.jsonl"):
    data += [json.loads(x) for x in open(f, "r")]

data_test = [line for line in data if line["year"] >= 2022]
data_train = [line for line in data if line["year"] < 2022]

def maim_language(data, langs):
    data_lang = [line for line in data if line["langs"] == langs]
    data_rest = [line for line in data if line["langs"] != langs]

    data_lang = sorted(data_lang, key=lambda x: x["score"])
    data_lang_top = data_lang[int(len(data_lang)*0.1):]
    data_lang_bot = data_lang[int(len(data_lang)*0.9)]

    return data_lang_top+data_rest, data_lang_bot+data_rest

# todo choose some lower-resource language that appears just once
data_ende_top, data_ende_bot = maim_language(data_train, "en-de")
data_enzh_top, data_enzh_bot = maim_language(data_train, "en-zh")