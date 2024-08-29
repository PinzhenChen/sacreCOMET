import json
from comet import download_model, load_from_checkpoint
import numpy as np
import random

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

data = [
    json.loads(line)
    for line in open("data/jsonl/test.jsonl")
]
data = random.Random(0).sample(data, k=1000)

data = [
    {
        "src": line["src"],
        "mt": line["tgt"],
        "ref": line["ref"],
    }
    for line in data
]

def test_model(batch_size, gpus):
    return np.array(model.predict(data, batch_size=batch_size, gpus=gpus).scores)

bs1_gpu1_base = test_model(1, 1)
bs1_gpu1 = test_model(1, 1)
bs64_gpu1 = test_model(64, 1)
bs1_gpu0 = test_model(1, 0)
bs64_gpu0 = test_model(64, 0)

print("bs1_gpu1-bs1_gpu1:  ", np.average(np.abs(bs1_gpu1 - bs1_gpu1_base)))
print("bs1_gpu1-bs64_gpu1: ", np.average(np.abs(bs64_gpu1 - bs1_gpu1_base)))
print("bs1_gpu1-bs1_gpu0:  ", np.average(np.abs(bs1_gpu0 - bs1_gpu1_base)))
print("bs64_gpu1-bs64_gpu0:", np.average(np.abs(bs64_gpu0 - bs64_gpu1)))