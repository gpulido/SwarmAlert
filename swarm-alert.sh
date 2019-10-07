#!/bin/bash -ex
python /src/swarm-alert.py  --check_interval "$CHECK_INTERVAL" \
     --whitelist "$WHITE_LIST" --blacklist "$BLACK_LIST" --msg_prefix "$MSG_PREFIX" --loglevel "$LOGGING_LEVEL"
## File : swarm-alert.sh ends
