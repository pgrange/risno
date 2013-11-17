#!/bin/bash

DIR=$(cd $(dirname $0); pwd)

cat << EOF
export PYTHONPATH=$PYTHONPATH:"$DIR"/test:"$DIR"/
# Run the following command to set your environment:
# eval \$($0)
EOF
