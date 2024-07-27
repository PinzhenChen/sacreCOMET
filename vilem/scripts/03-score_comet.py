from comet import load_from_checkpoint
import argparse
import json

args = argparse.ArgumentParser()
args.add_argument("model")
args.add_argument("data")
args = args.parse_args()

model = load_from_checkpoint(args.model)

data = [json.loads(x) for x in open(args.data, "r")]
data = [
    {
        "src": x["src"],
        "ref": x["ref"],
        "mt": x["tgt"],
    }
    for x in data
]
# TODO: try batch_size 64 and batch_size 1

model_output = model.predict(data, batch_size=32, gpus=1)
print("\n".join([str(x) for x in model_output["scores"]]))