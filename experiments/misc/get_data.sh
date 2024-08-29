#!/bin/bash

# Python 3.12.4
# pip install pip==24.1.2

mkdir -p data/
rm -rf data/
mkdir -p data/

# Get WMT files from sacrebleu

# pip install sacrebleu==2.4.2
# for yy in 22 23; do
#     mkdir -p data/wmt${yy}

#     for lang in de ru uk zh ; do

#         mkdir -p data/wmt${yy}/en-${lang}
#         sacrebleu -t wmt${yy} -l en-${lang} --echo src > data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.en
#         sacrebleu -t wmt${yy} -l en-${lang} --echo ref > data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${lang}

#         mkdir -p data/wmt${yy}/${lang}-en
#         sacrebleu -t wmt${yy} -l ${lang}-en --echo src > data/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.${lang}
#         sacrebleu -t wmt${yy} -l ${lang}-en --echo ref > data/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.en

#         for system in Online-A Online-B Online-G Online-W Online-Y; do
#             sacrebleu -t wmt${yy} -l en-${lang} --echo ${system} > data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${system}
#             sacrebleu -t wmt${yy} -l ${lang}-en --echo ${system} > data/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.${system}
#         done
#     done

#     mkdir -p data/wmt${yy}/cs-uk
#     sacrebleu -t wmt${yy} -l cs-uk --echo src > data/wmt${yy}/cs-uk/wmt${yy}.cs-uk.cs
#     sacrebleu -t wmt${yy} -l cs-uk --echo ref > data/wmt${yy}/cs-uk/wmt${yy}.cs-uk.uk

#     for system in Online-A Online-B Online-G Online-W Online-Y; do
#         sacrebleu -t wmt${yy} -l cs-uk --echo ${system} > data/wmt${yy}/cs-uk/wmt${yy}.cs-uk.${system}
#     done
# done


# Get WMT files from the metric task raw data
for yy in 22 23; do
    # edit the next line to point to the directory containing the raw data
    raw_data_dir=${some_directory_containing}/mt-metrics-eval-v2/wmt${yy}
    mkdir -p data/wmt${yy}

    for lang in de ru uk zh ; do

        mkdir -p data/wmt${yy}/en-${lang}
        cp ${raw_data_dir}/sources/en-${lang}.txt data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.en
        cp ${raw_data_dir}/references/en-${lang}.refA.txt data/wmt${yy}/en-${lang}/wmt${yy}.en-${lang}.${lang}

        mkdir -p data/wmt${yy}/${lang}-en
        cp ${raw_data_dir}/sources/${lang}-en.txt data/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.${lang}
        cp ${raw_data_dir}/references/${lang}-en.refA.txt data/wmt${yy}/${lang}-en/wmt${yy}.${lang}-en.en

        for lang_pair in ${lang}-en en-${lang}; do
            for system_file in ${raw_data_dir}/system-outputs/${lang_pair}/O*-*.txt; do
                cp ${system_file} data/wmt${yy}/${lang_pair}/wmt${yy}.${lang_pair}.$(basename ${system_file} .txt)
            done
        done

    done

    mkdir -p data/wmt${yy}/cs-uk
    cp ${raw_data_dir}/sources/cs-uk.txt data/wmt${yy}/cs-uk/wmt${yy}.cs-uk.cs
    cp ${raw_data_dir}/references/cs-uk.refA.txt data/wmt${yy}/cs-uk/wmt${yy}.cs-uk.uk

    for system_file in ${raw_data_dir}/system-outputs/${lang_pair}/O*-*.txt; do
        cp ${system_file} data/wmt${yy}/${lang_pair}/wmt${yy}.${lang_pair}.$(basename ${system_file} .txt)
    done

done