#!/bin/bash

# server command1 || true
# server command2 || true

server command1
if [ $? -ne 0 ]; then
    echo "server command1 failed"
    exit 1
fi

server command2
if [ $? -ne 0 ]; then
    echo "server command2 failed"
    exit 1
fi

# Keep the script running
tail -f /dev/null

