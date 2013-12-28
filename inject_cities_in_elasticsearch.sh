#!/bin/bash

function csv2bulk() {
  while read line
  do
    zip=$(echo $line | cut -d' ' -f1)
    name=$(echo $line | cut -d' ' -f2-)
    id=fr_${zip}_$(echo $name |\
                iconv -f UTF-8 -t US-ASCII -c |\
                sed -e 's:[^A-Za-z]:_:g')

    if echo ${name} | grep --silent -f city_unboost_terms.txt
    then city_boost="0.3"
    else city_boost="1.0"
    fi

    cat << EOF
{"index":{"_index":"cities","_type":"city","_id":"${id}"}}
{"name":"${name}","zipcode":"${zip}","name_suggest":{"input":"${name}","payload":"${id}"},"city_boost":${city_boost}}
EOF
  done
}

function bulk_insert() {
  curl -XPOST localhost:9200/_bulk --data-binary @-
}

curl -X DELETE localhost:9200/cities

curl -X PUT localhost:9200/cities -d '
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
     "stopwords" : [ "de", "du", "à", "a", "au", "en", "et", "le", "les", "sur", "m", "maison"],
     "ignore_case" : "true"
    },
    "synonyms_cities" : {
     "type" : "synonym",
     "synonyms" : [
      "st => saint",
      "ste => sainte"
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

cat cp-france.csv | csv2bulk | bulk_insert

