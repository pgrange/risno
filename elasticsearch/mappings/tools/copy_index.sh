#!/bin/bash

#load util functions
source $(dirname $0)/utils.sh

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <from_index> <to_index>\n" >&2
  printf "\tcopy <from_index> data inside <to_index>\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 2 ] || usage "missing parameter"

from_index=$1
to_index=$2

set $(init_scroll $from_index)
scroll_id=$1
total=$2

echo "$total documents to copy" >&2

i=1
while scroll ${scroll_id} | object2bulk ${to_index} | bulk_insert >/dev/null
do
  echo "$i bulk inserted" >&2
  i=$((i+1))
done

echo end of copy >&2

echo size of original index ${from_index}   : $(index_size ${from_index}) >&2
echo size of destination index ${to_index}: $(index_size ${to_index}) >&2
