#!/bin/bash
set -o pipefail

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <alias> <index>\n" >&2
  printf "\tdelete alias <alias> for index <index>\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 2 ] || usage "missing parameter"

alias=$1
index=$2

echo Please type \"yes\" to confirm before suppressing alias $alias for index $index
read confirmation

if [ "$confirmation" == "yes" ] 
then 
  curl -XPOST 'http://localhost:9200/_aliases' -d "
  {
   \"actions\" : [
    { \"remove\" : { \"index\" : \"${index}\", \"alias\" : \"${alias}\" } }
   ]
  }"
else
  echo cancelling
fi

