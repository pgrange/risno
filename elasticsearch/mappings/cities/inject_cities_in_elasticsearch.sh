#!/bin/bash

[[ -z ELASTIC_URL ]] && ELASTIC_URL="localhost:9200"

echo $ELASTIC_URL

install_dir=$(cd $(dirname $0) && pwd)

function csv2bulk() {
  while read line
  do
    zip=$(echo $line | cut -d' ' -f1)
    name=$(echo $line | cut -d' ' -f2-)
    id=fr_${zip}_$(echo $name |\
                iconv -f UTF-8 -t US-ASCII -c |\
                sed -e 's:[^A-Za-z]:_:g')

    if echo ${name} | grep --silent -f ${install_dir}/city_unboost_terms.txt
    then city_boost="0.3"
    else city_boost="1.0"
    fi

    cat << EOF
{"index":{"_index":"cities","_type":"city","_id":"${id}"}}
{"name":"${name}",\
 "zipcode":"${zip}",\
 "city_boost":${city_boost},\
 "name_suggest":{\
  "input":["${name}",\
           "${zip}",\
           "${name} ${zip}",\
           "${zip} ${name}"],\
  "output": "${name} (${zip})",\
  "payload":"${id}"}}
EOF
  done
}

function bulk_insert() {
  curl -XPOST $ELASTIC_URL/_bulk --data-binary @-
}

curl -X DELETE $ELASTIC_URL/cities

curl -X PUT $ELASTIC_URL/cities -d '
{
 "settings" : {
  "analysis" : {
   "analyzer" : {
    "city_name" : {
     "type" : "custom",
     "tokenizer" : "standard",
     "filter" : ["asciifolding", "lowercase", "elision", "synonyms_cities", "stopwords_cities", "unique"]
    }
   },
   "filter" : {
    "stopwords_cities" : {
     "type" : "stop",
     "stopwords" : [ "de", "du", "à", "a", "au", "en", "et", "le", "la", "les", "sur", "m", "maison"],
     "ignore_case" : "true"
    },
    "synonyms_cities" : {
     "type" : "synonym",
     "synonyms" : [
      "st => saint",
      "ste => sainte",
      "labrede => la brede"
     ]
    },
    "elision" : {
     "type" : "elision",
     "articles" : ["l", "m", "t", "qu", "n", "s", "j", "d"]
    }
   }
  }
 },
 "mappings" : {
  "city" : {
   "_boost": {"name" : "city_boost", "null_value" : "1.0"},
   "properties" : {
    "name" : { "type" : "string", "analyzer" : "city_name"},
    "zipcode": {"type": "string", "boost": 2.0},
    "name_suggest" : {
     "type" : "completion", "payloads" : true,
     "index_analyzer" :  "city_name",
     "search_analyzer" : "city_name",
     "preserve_position_increments": false,
     "preserve_separators": false
    }
   }
  }
 }
}'

cat ${install_dir}/cp-france.csv | csv2bulk | bulk_insert
