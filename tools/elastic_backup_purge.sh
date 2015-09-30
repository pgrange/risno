#!/bin/bash

a_month_ago=$(date -d '30 days ago' +%s000)

for snapshot in \
  $( curl localhost:9200/_snapshot/backup/_all \
     | jq -r ".snapshots[] \
              | if .start_time_in_millis < ${a_month_ago} \
                then .snapshot \
                else null end" \
     | grep -v '^null$' )
do
  curl -XDELETE localhost:9200/_snapshot/backup/$snapshot
done
