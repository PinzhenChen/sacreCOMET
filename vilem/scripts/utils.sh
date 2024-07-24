function get_config() {
    TRAIN_DATA=$(realpath $1)
    DEV_DATA=$(realpath data/da/general/train_head.csv)
    
    TMP_CONFIG_DIR=$(mktemp -d)
    cp configs/* ${TMP_CONFIG_DIR}
    cat configs/model.yaml \
        | sed "s|TRAIN_DATA_PATH|${TRAIN_DATA}|" \
        | sed "s|DEV_DATA_PATH|${DEV_DATA}|" \
        > ${TMP_CONFIG_DIR}/model.yaml
    echo ${TMP_CONFIG_DIR}/model.yaml
}

function sbatch_gpu() {
    JOB_NAME=$1;
    JOB_WRAP=$2;
    sbatch \
        -J $JOB_NAME --output=logs/%j.out --error=logs/%j.err \
        --gpus=1 --gres=gpumem:20g \
        --ntasks=6 --mem-per-cpu=4G --time=4-0 \
        --wrap="$JOB_WRAP";
}