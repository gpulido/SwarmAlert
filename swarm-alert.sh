#!/bin/bash -ex
python /src/swarm-alert.py  --check_interval "$CHECK_INTERVAL" \
       --user_key "$PUSHOVER_USER_KEY" --api_token "$PUSHOVER_API_TOKEN" --whitelist "$WHITE_LIST" \
    --blacklist "$BLACK_LIST" --msg_prefix "$MSG_PREFIX" --loglevel "$LOGGING_LEVEL"
## File : swarm-alert.sh ends
