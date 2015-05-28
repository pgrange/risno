#!/bin/bash

set -o pipefail

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <index>\n" >&2
  printf "\tdelete index <index>\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 1 ] || usage "missing parameter"

index=$1

echo Please type \"yes\" to confirm before suppressing index $index
read confirmation

if [ "$confirmation" == "yes" ] 
then 
  curl -f -XDELETE "localhost:9200/$index"
else
  echo cancelling
fi

