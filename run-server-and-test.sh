#!/bin/bash

# If file based logging is desired, use 
# LOG_TO_FILE=/path/to/file dev.sh

CBDIR=${CBDIR:=/node/data}
LOG_LEVEL=${LOG_LEVEL:=debug}
LOG_COLOURS=${LOG_COLOURS:=true}
LOG_FORMAT=${LOG_FORMAT:=standard}

# Launch the server
/usr/local/bin/crossbar start \
		      --cbdir ${CBDIR} \
		      --logformat ${LOG_FORMAT}\
		      --color ${LOG_COLOURS}\
		      --loglevel ${LOG_LEVEL} &

sleep 10

python test-case.py
