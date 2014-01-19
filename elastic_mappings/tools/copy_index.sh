#!/bin/bash

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <from_index> <to_index>\n" >&2
  printf "\tcopy <from_index> data inside <to_index>\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "suado apt-get install jq"

[ $# -eq 2 ] || usage "missing parameter"

from_index=$1
to_index=$2

function init_scroll() {
  curl -s -XGET "localhost:9200/${from_index}/_search?search_type=scan&prettyi&size=100&scroll=10m" -d '
  {
   "query": {"match_all" : {}}
  }' \
  | jq -r "._scroll_id,.hits.total"
}

function scroll() {
  scroll_id=$1
  curl -s -XGET 'localhost:9200/_search/scroll?scroll=10m' -d ${scroll_id} \
  | jq ".hits.hits | .[]"
}

function object2bulk() {
  jq -c "{index:{_index: \"${to_index}\",_type,_id}},._source"
}

function bulk_insert() {
  curl -fs -XPOST localhost:9200/_bulk --data-binary @-
}

function index_size() {
  index=$1
  curl -s -XGET "localhost:9200/${from_index}/_search?search_type=scan&prettyi&scroll=1" -d '
  {
   "query": {"match_all" : {}}
  }' \
  | jq -r ".hits.total"
}

set $(init_scroll)
scroll_id=$1
total=$2

echo "$total documents to copy"

i=0
while scroll ${scroll_id} | object2bulk | bulk_insert >/dev/null
do
  echo "$i bulk inserted"
  i=$((i+1))
done

echo end of copy

echo size of original index ${from_index}   : $(index_size ${from_index})
echo size of destination index ${from_index}: $(index_size ${to_index})
