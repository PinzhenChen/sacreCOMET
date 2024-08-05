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

    print()
    print(f"Python{PYTHON_VER}|Comet{COMET_VER}|{PRECISION}|{MODEL}")

def get_citation(args):
    import os
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


def cmd_entry():
    args = argparse.ArgumentParser(
        description=
        "Tool to guide you through reporting the use of COMET for machine translation evaluation."
        "Providing arguments in the command line will skip the interactive mode.\n"
        "Example: sacrecomet cite Unbabel/xcomet-xl.\n"
        "Example: sacrecomet --model xcomet-xl --precision fp16."
    )
    args.add_argument(
        "command", type=str, default=None, nargs="*"
    )
    args.add_argument("--precision", "--prec", "-p", type=str, default=None)
    args.add_argument("--model", "-m", type=str, default=None)
    args = args.parse_args()

    if not args.command or args.command[0] in {"ver", "version"}:
        if len(args.command) > 1:
            eprint("Too many arguments for signature command.")
            sys.exit(1)
        get_version(args)
    elif args.command and args.command[0] in {"cite", "bib", "citation"}:
        if len(args.command) > 2:
            eprint("Too many arguments for citation command.")
            sys.exit(1)
        if len(args.command) == 2:
            args.model = args.command[1]
        get_citation(args)