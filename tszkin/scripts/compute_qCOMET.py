import argparse
import csv
import os
import time
import warnings

import torch
import torch.ao.quantization

from comet import download_model, load_from_checkpoint

#Compute COMET using model.predict with 
# different numerical precisions under GPU/CPU


def read_tsv(path):
    #read the .tsv file into a list of dicts
    data = []
    with open(path, "r") as fin:
        csv_reader = csv.DictReader(fin, delimiter="\t")
        for row in csv_reader:
            data.append({
                "src": row["src"],
                "mt": row["tgt"],
                "ref": row["ref"]}
            )
    return data


def write_segmentscores_to_tsv(inFile_path, output_prefix, segment_scores):
    #Append a segment scores column to the original tsv file
    with open(inFile_path, "r") as fin:
        reader = csv.reader(fin, delimiter="\t")
        data = list(reader)

    data[0].append("comet_score")

    for i in range(1, len(data)):
        data[i].append(segment_scores[i-1])

    with open(output_prefix+".comet_segment_score.tsv", "w") as fo:
        writer = csv.writer(fo, delimiter="\t")
        writer.writerows(data)


def write_systemscore_to_tsv(output_prefix, system_score):
    with open(output_prefix+".comet_system_score.tsv", "w") as fo:
        fo.write(f"{system_score}\n")


def write_miscInfo_to_tsv(output_prefix, model_size, proc_time):
    with open(output_prefix+".size_time.tsv", "w") as fo:
        fo.write(f"size in MB: {model_size:.2f}\n")
        fo.write(f"proc time in seconds: {proc_time}\n")


def get_model_size(model, lang, dtype):
    print(f"getting model size - tmp_{lang}_{dtype}.pt")
    torch.save(model.state_dict(), f"tmp_{lang}_{dtype}.pt")
    size = os.path.getsize(f'tmp_{lang}_{dtype}.pt')/1e6 
    os.remove(f'tmp_{lang}_{dtype}.pt')
    return size


def dyquant_model_dtype_to(model, dtype):
    """
    https://pytorch.org/docs/2.1/quantization.html#module-torch.ao.quantization

    Note: 
     1) this package only supports CPU
     2) quite a lot of layers cannot be quantized (check their doc)
    """

    if dtype == "float16":
        #model.half() and model.to(torch.bfloat) don't work in CPU
        # ->RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'

        #For neligible effect on model size reduction, see 
        #https://discuss.pytorch.org/t/float16-dynamic-quantization-has-no-model-size-benefit/99675
        model = torch.ao.quantization.quantize_dynamic(
            model,
            dtype=torch.float16,
            inplace=False
        )
    elif dtype == "qint8":
        model = torch.ao.quantization.quantize_dynamic(
            model,
            dtype=torch.qint8,
            inplace=False
        )
    else:
        if dtype != "float32":
            raise ValueError("dtype must be either 'float32', 'float16' or 'qint8'")

    return model 

def quant_model_dtype_to(model, dtype):
    if dtype == "float16":
        #model.half()
        #RuntimeError: mat1 and mat2 must have the same dtype, but got Float and Half

        #TszKin: By adding "self.model.half()" in the below line, it works
        # https://github.com/Unbabel/COMET/blob/master/comet/encoders/xlmr.py#L51
        warnings.warn("Change the source code for float16. If not, -> float32")
    return model


def main(args):
    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)

    #LANGS = ["en-de", "en-zh", "de-en", "zh-en"]
    print(f"DTYPES: {args.dtypes}")
    print(f"LANGS: {args.langs}")

    if args.gpus == 1:
        assert torch.cuda.is_available()
        for dtype in args.dtypes:
            assert dtype == "float32" or dtype == "float16"
        quantize = quant_model_dtype_to
    elif args.gpus == 0:
        quantize = dyquant_model_dtype_to
    else:
        raise ValueError()

    for lang in args.langs:
        inFile = ".".join([args.file_prefix, lang, "tsv"])
        data = read_tsv(inFile)

        for dtype in args.dtypes:
            model_q = quantize(model, dtype=dtype)
            model_size = get_model_size(model_q, lang, dtype)

            start = time.time()
            pred =  model_q.predict(data, batch_size=8, gpus=args.gpus)
            proc_time = time.time() - start


            #Write
            output_prefix = f"output.{lang}.{dtype}_gpu{args.gpus}"
            write_segmentscores_to_tsv(
                inFile_path=inFile, 
                output_prefix=output_prefix, 
                segment_scores=pred[0]
            )

            write_systemscore_to_tsv(output_prefix, system_score=pred[1])
            write_miscInfo_to_tsv(output_prefix, model_size, proc_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_prefix", type=str,
        help="e.g. xxx/output from xxx/output.[lang].tsv"
    )
    parser.add_argument(
        "--langs", type=str, nargs="+",
        help="e.g. en-de, de-en"
    )
    parser.add_argument(
        "--gpus", type=int, choices=[0, 1],
        help='0: cpu->dynamic_quantization; 1: gpu'
    )
    parser.add_argument(
        "--dtypes", type=str, nargs="+",
        choices=['float16', 'float32', 'qint8'],
        help="CPU, support 'float32', 'float16' and 'qint8' \
        via the torch.quantization. \
        GPU, support 'float32' and 'float16'. GPU-float16, \
        requires changing the source code explicitly."
    )
    args = parser.parse_args()

    main(args)
