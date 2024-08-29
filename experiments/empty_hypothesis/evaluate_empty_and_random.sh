#!/bin/bash

# Python 3.12.4
pip install pip==24.1.2
pip install unbabel-comet==2.2.2

export CUDA_VISIBLE_DEVICES=4,5,6,7

function random_sample {
  num_lines=$(wc -l < "$1")
  for i in $(seq $num_lines); do
    shuf -n 1 "$2"
  done
}

data_folder=../data

log_file=log_comet2.2.2-empty-random.txt
rm -f ${log_file}
touch ${log_file}

for comet_model in Unbabel/wmt22-comet-da Unbabel/wmt22-cometkiwi-da ; do
  echo "Model: ${comet_model}" >> ${log_file}
  for yy in 23 ; do
      for lang in de zh ; do

          src_file=${data_folder}/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.en
          ref_file=${data_folder}/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${lang}

          empty_file_name=temp_empty_file.txt
          touch ${empty_file_name}
          lines=$(wc -l ${src_file} | cut -d' ' -f1)

          for i in $(seq 1 ${lines}); do
              echo "" >> ${empty_file_name}
          done

          wmt22_ref_file=${data_folder}/wmt22/en-${lang}/wmt22.en-${lang}.${lang}
          random_file=temp_random_file.txt
          random_sample ${ref_file} ${wmt22_ref_file} > ${random_file}

          hyp_files=temp_data_*.txt
          wc -l ${src_file} ${ref_file} ${hyp_files}
          comet-score \
              -s ${src_file} -r ${ref_file} \
              --model ${comet_model} \
              --quiet --only_system --gpus 4 \
              -t ${hyp_files} >> ${log_file}

          rm -f ${hyp_files}
      done
  done
done