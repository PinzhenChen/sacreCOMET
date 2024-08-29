#!/bin/bash

conda activate testCOMET_py3.8.5

prefix=$1 #e.g. ../data/output
OMP_NUM_THREADS=16 python compute_qCOMET.py \
	--file_prefix ${prefix} \
	--langs "en-de" "de-en" \
	--gpus 0 \
	--dtypes "float32" "float16" "qint8"

conda deactivate
