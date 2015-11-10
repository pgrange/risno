#!/bin/bash

set -o pipefail

curl_opt="-fs"

[[ -z $ELASTIC_DB ]] && ELASTIC_DB='localhost:9200'
index=ads
type=immo
older_than="now-1d"

function old_ads_init_scroll() {
  curl "$curl_opt" -XGET "${ELASTIC_DB}/${index}/${type}/_search?search_type=scan&pretty&size=1000&scroll=10m" -d "
  {
    \"query\": {
      \"filtered\": {
        \"filter\": {  
          \"missing\": {\"field\": \"expired\"}
        },
        \"filter\": {
          \"range\": {
            \"_timestamp\": {\"lt\": \"$older_than\"}
          }
        }
      }
    }
  }" \
  | jq -r "._scroll_id,.hits.total"
}

function scroll() {
  local scroll_id=$1
  curl "$curl_opt" -XGET "${ELASTIC_DB}/_search/scroll?scroll=10m" -d ${scroll_id} \
  | jq ".hits.hits | .[]"
}

function object2bulk() {
  local to_index=$1
  jq -c "if .fields then
          {index:({_index: \"${to_index}\",_type,_id} + .fields)}
         else
          {index:{_index: \"${to_index}\",_type,_id}}
         end,
         if .__extra then ._source + .__extra else ._source end"
}

function bulk_insert() {
  curl "$curl_opt" -XPOST ${ELASTIC_DB}/_bulk --data-binary @-
}

function expire() {
  jq -c ". + {__extra: {expired: true}}"
}

set $(old_ads_init_scroll ${index})
scroll_id=$1
total=$2

echo "$total ads to expire" >&2

i=0
while scroll ${scroll_id} | expire | object2bulk ${index} | bulk_insert > /dev/null
do
  echo "$i bulk updated" >&2
  i=$((i+1))
done

echo "Done." >&2
