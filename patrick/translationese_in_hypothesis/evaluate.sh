#!/bin/bash

# Python 3.12.4
pip install pip==24.1.2
pip install unbabel-comet==2.2.2

export CUDA_VISIBLE_DEVICES=4,5,6,7

log_file=log_comet2.2.2-translationese-hypothesis.txt
rm -f ${log_file}
touch ${log_file}

for comet_model in Unbabel/wmt22-cometkiwi-da Unbabel/wmt22-comet-da ; do
    echo "Model: ${comet_model}" >> ${log_file}
    src_file=src.txt
    ref_file=ref.txt

    hyp_files_orig=systems/*.txt
    hyp_files_para=paraphrased/*.txt

    wc -l ${src_file} ${ref_file} ${hyp_files_orig} ${hyp_files_para}

    comet-score \
        -s ${src_file} -r ${ref_file} \
        --model ${comet_model} \
        --quiet --only_system --gpus 4 \
        -t ${hyp_files_orig} ${hyp_files_para} >> ${log_file}
done