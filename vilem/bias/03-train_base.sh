. scripts/utils.sh

sbatch_gpu "zori_base" "comet-train --cfg $(get_config 'data/csv/train.csv' 'zori_base')"

sbatch_gpu "zori_en-de.bot-flat" "comet-train --cfg $(get_config 'data/csv/train.en-de.bot-flat.csv' 'zori_en-de.bot-flat')"
sbatch_gpu "zori_en-de.bot-sys" "comet-train --cfg $(get_config 'data/csv/train.en-de.bot-sys.csv' 'zori_en-de.bot-sys')"
sbatch_gpu "zori_en-de.top-flat" "comet-train --cfg $(get_config 'data/csv/train.en-de.top-flat.csv' 'zori_en-de.top-flat')"
sbatch_gpu "zori_en-de.top-sys" "comet-train --cfg $(get_config 'data/csv/train.en-de.top-sys.csv' 'zori_en-de.top-sys')"