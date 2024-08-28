for file in data/* ; do
    echo "Paraphrasing $file"
    python3 gpt_paraphrase.py -i $file
done