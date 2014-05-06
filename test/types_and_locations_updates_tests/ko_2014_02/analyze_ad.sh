#!/bin/bash

function analyse() {
  query="$1"
  curl -sf -XGET "localhost:9299/types/_analyze?field=type.french" -d "$query" \
  | jq '.tokens[]|.token'
}

file="$1"
id="$2"

echo "---location---"
analyse "$(grep "^$id;" $file | cut -d';' -f4)"

echo "---description---"
analyse "$(grep "^$id;" $file | cut -d';' -f5-)"
