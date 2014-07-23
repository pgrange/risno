#!/bin/bash -x

#load util functions
source $(pwd $0)/utils.sh

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "elasticsearch_bulk_insert_generator | $0\n" >&2
  printf "\tinserts data received on stdin into elasticsearch\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 0 ] || usage "invalid parameters"

bulk_insert
