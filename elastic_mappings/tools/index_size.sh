#!/bin/bash

#load util functions
source $(pwd $0)/utils.sh

function usage() {
  printf "$1\n" >&2
  printf "\n"
  printf "$0 <index>\n" >&2
  printf "\tdisplay size of index <index>\n" >&2

  exit 1
}

[ ! $(which jq) ] && usage "sudo apt-get install jq"

[ $# -eq 1 ] || usage "missing parameter"

index=$1

index_size $index
