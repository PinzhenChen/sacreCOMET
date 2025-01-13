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

    if args.references is None:
        REFERENCES = input("How many references did you use and how did you aggregated them? E.g. '1' or '2avg'.\n")
    else:
        REFERENCES = args.references

    eprint()
    print(f"Python{PYTHON_VER}|Comet{COMET_VER}|{PRECISION}|{MODEL}|r{REFERENCES}")

def get_citation(args):
    from papers import PAPERS

    if args.model is None:
        MODEL = input("Which model did you use? Provide huggingface identifier (Unbabel/...).\n")
    else:
        MODEL = args.model

    orig_model = MODEL
    
    # try to normalize
    MODEL = MODEL.removeprefix("/").lower()
    if not MODEL.startswith("unbabel/"):
        MODEL = f"unbabel/{MODEL}"

    if MODEL not in PAPERS:
        eprint(f"Model {orig_model} not found in papers.json, defaulting to the original COMET paper.")
        MODEL = "default"
    
    print(PAPERS[MODEL]["url"]+"\n")
    print(PAPERS[MODEL]["citation"])

def get_models():
    from papers import PAPERS
    print("\n".join(PAPERS.keys()))

def cmd_entry():
    args = argparse.ArgumentParser(
        description=
        "Tool to guide you through reporting the use of COMET for machine translation evaluation."
        "Providing arguments in the command line will skip the interactive mode.\n"
        "Example: sacrecomet cite --model Unbabel/xcomet-xl.\n"
        "Example: sacrecomet --model xcomet-xl --precision fp16.\n"
        "Example: sacrecomet list."
    )
    args.add_argument(
        "command", type=str, default=None,
        choices=["ver", "version", "cite", "bib", "citation", "models", "list"],
        nargs="?"
    )
    args.add_argument("--precision", "--prec", type=str, default=None)
    args.add_argument("--references", type=str, default=None)
    args.add_argument("--model", "-m", type=str, default=None)
    args = args.parse_args()

    if args.command is None or args.command in {"ver", "version"}:
        get_version(args)
    elif args.command in {"cite", "bib", "citation"}:
        if args.model is None:
            eprint("Please provide a model that you wish to cite.")
        get_citation(args)
    elif args.command in {"models", "list"}:
        get_models()