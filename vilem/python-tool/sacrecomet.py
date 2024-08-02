import argparse
import sys

def cmd_entry():
    args = argparse.ArgumentParser(
        description=
        "Tool to guide you through reporting the use of COMET for machine translation evaluation."
        "Providing arguments in the command line will skip the interactive mode."
    )
    args.add_argument("--precision", type=str, default=None)
    args.add_argument("--model", type=str, default=None)
    args = args.parse_args()

    eprint = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)
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