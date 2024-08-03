import argparse
import sys

eprint = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)

def get_version(args):
    eprint("Detecting local environment...")
    
    PYTHON_VER = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    try:
        import comet
    except ImportError:
        eprint("COMET is not installed. Install it with `pip install unbabel-comet`.")
        sys.exit(1)
    COMET_VER = comet.__version__

    signature = f"Python{PYTHON_VER}|Comet{COMET_VER}"
    eprint(signature + " ...")

    if args.precision is None:
        PRECISION = input("Which precision did you use? [ENTER for default fp32]:\n")
        if PRECISION == "":
            PRECISION = "fp32"
    else:
        PRECISION = args.precision

    if args.model is None:
        MODEL = input("Which model did you use? Provide accessible link (https://...), huggingface identifier (Unbabel/...), or description of local model.\n")
    else:
        MODEL = args.model

    print()
    print(f"{signature}|{PRECISION}|{MODEL}")

def get_citation(args):
    import os
    import json
    papers = "/".join(os.path.realpath(__file__).split("/")[:-1])+"/papers.json"
    papers = json.load(open(papers, "r"))

    if args.model is None:
        MODEL = input("Which model did you use? Provide huggingface identifier (Unbabel/...).\n")
    else:
        MODEL = args.model

    orig_model = MODEL
    
    # try to normalize
    MODEL = MODEL.removeprefix("/").lower()
    if not MODEL.startswith("unbabel/"):
        MODEL = f"unbabel/{MODEL}"

    if MODEL not in papers:
        eprint(f"Model {orig_model} not found in papers.json, defaulting to the original COMET paper.")
        MODEL = "default"
    
    print(papers[MODEL]["url"]+"\n")
    print(papers[MODEL]["citation"])


def cmd_entry():
    args = argparse.ArgumentParser(
        description=
        "Tool to guide you through reporting the use of COMET for machine translation evaluation."
        "Providing arguments in the command line will skip the interactive mode."
    )
    args.add_argument(
        "command", type=str, default=None, nargs="?",
        choices=[None, "ver", "version", "cite", "bib", "citation"]
    )
    args.add_argument("--precision", type=str, default=None)
    args.add_argument("--model", type=str, default=None)
    args = args.parse_args()

    if args.command in {None, "ver", "version"}:
        get_version(args)
    elif args.command in {"cite", "bib", "citation"}:
        get_citation(args)