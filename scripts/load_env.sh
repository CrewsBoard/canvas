#!/bin/bash

ENV=${1:-dev}

echo "Generating environment variables for $ENV environment"

yaml_to_env() {
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
    sed -ne "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\([^#]*\).*$s\$|\1$fs\2$fs\3|p" $1 |
    awk -F$fs '{
        indent = length($1)/2;
        vname[indent] = $2;
        for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=\"%s\"\n", "'$prefix'", vn, $2, $3);
        }
    }' | sed 's/^_//'
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

if [ ! -f $CONFIG_FILE ]; then
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

echo "Loading environment variables from $CONFIG_FILE"

while IFS= read -r line; do
    if [[ $line =~ ^[a-zA-Z_][a-zA-Z0-9_]*= ]]; then
        eval "$line"
    fi
done < <(yaml_to_env $CONFIG_FILE)

export APP_NAME=$app_name
export VITE_API_URL=$ui_vite_api_url

export POSTGRES_PORT=$database_port
export POSTGRES_DB_NAME=$database_db_name
export POSTGRES_USER_NAME=$database_username
export POSTGRES_PASSWORD=$database_password

export MSG_BROKER_REDIS_PORT=$msg_broker_redis_port
export MSG_BROKER_REDIS_PASSWORD=$msg_broker_redis_password

export MSG_BROKER_RABBITMQ_PORT=$msg_broker_rabbitmq_port
export MSG_BROKER_RABBITMQ_UI_PORT=$msg_broker_rabbitmq_ui_port
export MSG_BROKER_RABBITMQ_USERNAME=$msg_broker_rabbitmq_username
export MSG_BROKER_RABBITMQ_PASSWORD=$msg_broker_flow_engine_node_msg_processor_password

echo "All environment variables loaded successfully."
