#!/bin/bash -ex
python /swarm-alert.py  --check_interval "$CHECK_INTERVAL" \
       --token "$PUSHOVER_TOKEN" --app_key "$PUSHOVER_APP_KEY" --whitelist "$WHITE_LIST" \
    --blacklist "$BLACK_LIST" --msg_prefix "$MSG_PREFIX" --loglevel "$LOGGING_LEVEL"
## File : swarm-alert.sh ends
