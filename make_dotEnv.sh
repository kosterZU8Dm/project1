#!/bin/bash

ENV_FILE="./.env"

touch $ENV_FILE
cat <<EOF > $ENV_FILE
MONGO_URI = "mongodb://xxx:27017/xxx"
COLLECTION_NAME = "xxx"
EOF
