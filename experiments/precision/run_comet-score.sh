#!/bin/bash

#Check the scores using comet-score entry point

conda activate testCOMET_py3.8.5
export CUDA_VISIBLE_DEVICES=1

for lang in {en-de,de-en,en-zh,zh-en}; do
	f=output.${lang}.tsv
	cut -f1 ${f} | tail -n +2 > tmp_src.txt
	cut -f3 ${f} | tail -n +2 > tmp_tgt.txt
	cut -f2 ${f} | tail -n +2 > tmp_ref.txt

	comet-score -s tmp_src.txt -t tmp_tgt.txt -r tmp_ref.txt > cometscore.${lang}.txt
	rm tmp_src.txt tmp_tgt.txt tmp_ref.txt
done

conda deactivate
