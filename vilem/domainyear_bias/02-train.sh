. scripts/utils.sh

sbatch_gpu "tagdomain" "comet-train --cfg $(get_config 'data/csv/train.tagdomain.csv' 'tagdomain')"
sbatch_gpu "tagyear" "comet-train --cfg $(get_config 'data/csv/train.tagyear.csv' 'tagyear')"