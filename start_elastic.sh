#!/bin/bash

# Load configuration
. etc/risnorc
if [ ! -d $RISNO_DIR ]
then
    echo "Creates Risno directory"
    mkdir -p $RISNO_DIR/elastic-storage/log
    mkdir -p $RISNO_DIR/elastic-storage/data
fi

# Start container
docker run -d -p 9200:9200 -v $RISNO_DIR/elastic-storage/log/:/var/log/elasticsearch -v $RISNO_DIR/elastic-storage/data/:/var/lib/elasticsearch/ pgrange/elasticsearch
