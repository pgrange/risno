#!/bin/bash

#load util functions
source $(dirname $0)/utils.sh

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <from_file>\n" >&2
  printf "\timport <from_file> data inside elasticsearch\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 1 ] || usage "missing parameter"

from_file=$1

total=$(( $(wc -l $from_file | cut -d' ' -f1) / 2 ))
echo "$total documents to import" >&2

cat $from_file | bulk_insert

echo end of import >&2

echo size of original file ${from_file}   : $total >&2
