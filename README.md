# SacreCOMET &nbsp;&nbsp;&nbsp; [![PyPI Version](https://img.shields.io/pypi/v/sacrecomet)](https://pypi.org/project/sacrecomet/) [![test sacrecomet](https://github.com/PinzhenChen/sacreCOMET/actions/workflows/test.yml/badge.svg)](https://github.com/PinzhenChen/sacreCOMET/actions/workflows/test.yml)

> Since its introduction, the COMET metric has blazed a trail in the machine translation community, given its strong correlation with human judgements of translation quality. Its success stems from being a modified pre-trained multilingual model finetuned for quality assessment. However, it being a machine learning model also gives rise to a new set of pitfalls that may not be widely known. We investigate these unexpected behaviours from three aspects: 1) technical: obsolete software versions and compute precision; 2) data: empty content, language mismatch, and translationese at test time as well as distribution and domain biases in training; 3) usage and reporting: multi-reference support and model referencing in the literature. All of these problems imply that COMET scores is not comparable between papers or even technical setups and we put forward our perspective on fixing each issue. Furthermore, we release the SacreCOMET package that can generate a signature for the software and model configuration as well as an appropriate citation. The goal of this work is to help the community make more sound use of the COMET metric.

Read the full paper [Pitfalls and Outlooks in Using COMET](https://aclanthology.org/2024.wmt-1.121/).

## Tool

The Python tool has two functionalities.
First, it creates a signature with your setup and COMET model:

```
pip install sacrecomet

# Without anything will try to detect the local environment and will
# ask you questions about which COMET model you used.
# Example output: Python3.11.8|Comet2.2.2|fp32|unite-mup

sacrecomet 

# Arguments can also be specified non-interactively:

sacrecomet --model unite-mup --prec fp32
```

The other functionality is to find specific citations for COMET models that you're using:

```
sacrecomet cite --model Unbabel/xcomet-xl

https://arxiv.org/abs/2310.10482
@misc{guerreiro2023xcomet,
    title={xCOMET: Transparent Machine Translation Evaluation through Fine-grained Error Detection}, 
    ...
```

You can also list all the available models:
```
sacrecomet list

unbabel/wmt24-qe-task2-baseline
unbabel/wmt22-cometkiwi-da
unbabel/xcomet-xl
unbabel/xcomet-xxl
unbabel/towerinstruct-13b-v0.1
unbabel/towerinstruct-7b-v0.2
unbabel/towerbase-7b-v0.1
...
```

## Experiments

Documentation TODO

## Paper

Cite as:

```
@inproceedings{zouhar-etal-2024-pitfalls,
    title = "Pitfalls and Outlooks in Using {COMET}",
    author = "Zouhar, Vil{\'e}m and Chen, Pinzhen  and Lam, Tsz Kin  and Moghe, Nikita  and Haddow, Barry",
    editor = "Haddow, Barry and Kocmi, Tom  and Koehn, Philipp  and Monz, Christof",
    booktitle = "Proceedings of the Ninth Conference on Machine Translation",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.wmt-1.121/",
    doi = "10.18653/v1/2024.wmt-1.121",
    pages = "1272--1288",
}

```

<img src="https://raw.githubusercontent.com/PinzhenChen/sacreCOMET/main/misc/poster.png" width="900vw">

## YouTube presentation (click image)

[<img src="https://img.youtube.com/vi/jDMvueySuPo/maxresdefault.jpg" width=400px>](https://www.youtube.com/watch?v=jDMvueySuPo)

## Changelog

- v1.0.1 (13 January 2025)
  - Stable release
- v0.1.1 (13 January 2025)
  - Add `r` in the signature before references.
  - Add simple tests.
- v0.1.0 (30 October 2024):
  - Add `list` command to list available models
  - Add references usage to the SacreCOMET usage.
  - Deprecate `sacrecomet cite model_name` positional model name specification. Citations now have to explicitly use the `--model` argument.
- v0.0.1 (7 August 2024)
  - First release
