#!/bin/bash -ex
python /swarm-alert.py  --check_interval "$CHECK_INTERVAL" \
       --token "$PUSHOVER_TOKEN" --app_key "$PUSHOVER_APP_KEY" --whitelist "$WHITE_LIST" \
    --msg_prefix "$MSG_PREFIX"
## File : swarm-alert.sh ends
