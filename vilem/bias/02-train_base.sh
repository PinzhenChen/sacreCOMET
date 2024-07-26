. scripts/utils.sh

sbatch_gpu "zori_base" "comet-train --cfg $(get_config 'data/csv/train.csv')"