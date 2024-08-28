#!/bin/bash

# Python 3.12.4
# pip install pip==24.1.2
# pip install unbabel-comet==2.2.2

export CUDA_VISIBLE_DEVICES=0,1,2,3

data_folder=../data

log_file=log_comet2.2.2-wmt22da-software-versions.txt
rm -f ${log_file}
touch ${log_file}

for yy in 23 ; do

    for lang in de zh ; do

        # en->X
        src_file=${data_folder}/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.en
        ref_file=${data_folder}/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${lang}
        if [[ $(wc -l ${src_file} | cut -d" " -f1) -eq 0 ]] || [[ $(wc -l ${ref_file} | cut -d" " -f1) -eq 0 ]]; then
            continue
        fi

        hyp_file_prefix=${data_folder}/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.*
        hyp_files=$(ls ${hyp_file_prefix} | xargs -n 1 -I {} bash -c '[[ $(wc -l {} | cut -d" " -f1) -gt 0 ]] && echo {}')
        
        wc -l ${src_file} ${ref_file} ${hyp_files}
        comet-score \
            -s ${src_file} -r ${ref_file} \
            --model Unbabel/wmt22-comet-da \
            --quiet --only_system --gpus 4 \
            -t ${hyp_files} >> ${log_file}

        # X->en
        src_file=${data_folder}/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.${lang}
        ref_file=${data_folder}/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.en
        if [[ $(wc -l ${src_file} | cut -d" " -f1) -eq 0 ]] || [[ $(wc -l ${ref_file} | cut -d" " -f1) -eq 0 ]]; then
            continue
        fi

        hyp_file_prefix=${data_folder}/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.*
        hyp_files=$(ls ${hyp_file_prefix} | xargs -n 1 -I {} bash -c '[[ $(wc -l {} | cut -d" " -f1) -gt 0 ]] && echo {}')

        wc -l ${src_file} ${ref_file} ${hyp_files}
        comet-score \
            -s ${src_file} -r ${ref_file} \
            --model Unbabel/wmt22-comet-da \
            --quiet --only_system --gpus 4 \
            -t ${hyp_files} >> ${log_file}
    done
done