#!/bin/bash

# Python 3.12.4
pip install pip==24.1.2
pip install unbabel-comet==2.2.2

export CUDA_VISIBLE_DEVICES=0,1,2,3

log_file=log_comet2.2.2-lang-mismatch.txt
rm -f ${log_file}
touch ${log_file}

for yy in 23 ; do
    for lang in ru uk zh ; do
        # only en->X
        src_file=data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.en
        ref_file=data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${lang}

        hyp_files="data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.ru data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.uk data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.zh"
        
        wc -l ${src_file} ${ref_file} ${hyp_files}
        comet-score \
            -s ${src_file} -r ${ref_file} \
            --model Unbabel/wmt22-comet-da \
            --quiet --only_system --gpus 4 \
            -t ${hyp_files} >> ${log_file}

    done
done