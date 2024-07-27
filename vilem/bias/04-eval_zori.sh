. scripts/utils.sh

sbatch_gpu "eval_zori_base" "python3 scripts/03-score_comet.py models/zori_base.ckpt data/jsonl/test.jsonl"
sbatch_gpu "eval_zori_en-de.bot-flat" "python3 scripts/03-score_comet.py models/zori_en-de.bot-flat.ckpt data/jsonl/test.jsonl"
sbatch_gpu "eval_zori_en-de.bot-sys" "python3 scripts/03-score_comet.py models/zori_en-de.bot-sys.ckpt data/jsonl/test.jsonl"
sbatch_gpu "eval_zori_en-de.top-flat" "python3 scripts/03-score_comet.py models/zori_en-de.top-flat.ckpt data/jsonl/test.jsonl"
sbatch_gpu "eval_zori_en-de.top-sys" "python3 scripts/03-score_comet.py models/zori_en-de.top-sys.ckpt data/jsonl/test.jsonl"