#!/bin/bash

#load util functions
source $(dirname $0)/utils.sh

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <index>\n" >&2
  printf "\tdump <index> data to stdout in raw format\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 1 ] || usage "missing parameter"

index=$1

set $(init_scroll $index)
scroll_id=$1
total=$2

echo "$total documents to dump" >&2

i=0
while scroll ${scroll_id} | jq -c .
do
  echo "$i bulk dumped" >&2
  i=$((i+1))
done

echo end of dump >&2
