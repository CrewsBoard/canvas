#!/bin/bash

ENV=${1:-dev}

yaml_to_env() {
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
    sed -ne "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p" $1 |
    awk -F$fs '{
        indent = length($1)/2;
        vname[indent] = $2;
        for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=\"%s\"\n", "'$prefix'", vn, $2, $3);
        }
    }'
}

case $ENV in
    "dev")
        CONFIG_FILE="core/configs/dev.yaml"
        ;;
    "prod")
        CONFIG_FILE="core/configs/prod.yaml"
        ;;
    "stage")
        CONFIG_FILE="core/configs/stage.yaml"
        ;;
    *)
        echo "Invalid environment: $ENV"
        exit 1
        ;;
esac

eval $(yaml_to_env $CONFIG_FILE)

export APP_NAME=$app_name
export POSTGRES_USER=$database_user
export POSTGRES_PASSWORD=$database_password
export POSTGRES_DB=$database_db
export VITE_API_URL=$ui_vite_api_url
