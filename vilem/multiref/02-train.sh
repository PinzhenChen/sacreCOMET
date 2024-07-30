. scripts/utils.sh

sbatch_gpu "swap50" "comet-train --cfg $(get_config 'data/csv/train.swap50.csv' 'swap50')"