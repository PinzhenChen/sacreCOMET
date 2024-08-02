import json
import argparse
import numpy as np

args = argparse.ArgumentParser()
args.add_argument('data')
args = args.parse_args()

data_pred = [float(x.strip()) for x in open(args.data)]
data_test = [json.loads(x) for x in open("data/jsonl/test.jsonl")]

assert len(data_pred) == len(data_test)

print(
    "EN-DE",
    f'{np.average([pred for line, pred in zip(data_test, data_pred) if line["langs"] == "en-de"]):.5f}',
    f"({np.average([x['score'] for x in data_test if x['langs'] == 'en-de']):.5f})",
)
print(
    "EN-ZH",
    f'{np.average([pred for line, pred in zip(data_test, data_pred) if line["langs"] == "en-zh"]):.5f}',
    f"({np.average([x['score'] for x in data_test if x['langs'] == 'en-zh']):.5f})",
)