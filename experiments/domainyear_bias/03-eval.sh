. scripts/utils.sh

sbatch_gpu "eval_tagyear_2018" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2018.jsonl"
sbatch_gpu "eval_tagyear_2019" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2019.jsonl"
sbatch_gpu "eval_tagyear_2020" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2020.jsonl"
sbatch_gpu "eval_tagyear_2021" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2021.jsonl"
sbatch_gpu "eval_tagyear_2022" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2022.jsonl"
sbatch_gpu "eval_tagyear_2023" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2023.jsonl"
sbatch_gpu "eval_tagyear_2024" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2024.jsonl"
sbatch_gpu "eval_tagyear_2025" "python3 scripts/03-score_comet.py models/tagyear.ckpt data/jsonl/test.tagyear.2025.jsonl"

sbatch_gpu "eval_tagdomain_news" "python3 scripts/03-score_comet.py models/tagdomain.ckpt data/jsonl/test.tagdomain.news.jsonl"
sbatch_gpu "eval_tagdomain_flores" "python3 scripts/03-score_comet.py models/tagdomain.ckpt data/jsonl/test.tagdomain.flores.jsonl"
sbatch_gpu "eval_tagdomain_wiki" "python3 scripts/03-score_comet.py models/tagdomain.ckpt data/jsonl/test.tagdomain.wiki.jsonl"

# average scores
for f in logs/*_tag*.out; do
    echo $f;
    awk '{s+=$1}END{print s/NR/100}' RS=" " $f;
done