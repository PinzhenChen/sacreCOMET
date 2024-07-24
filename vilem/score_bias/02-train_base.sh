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

comet-train --cfg $(get_config "data/da/general/train.csv")