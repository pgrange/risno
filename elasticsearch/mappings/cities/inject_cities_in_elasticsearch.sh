#!/bin/bash

[[ -z $ELASTIC_URL ]] && ELASTIC_URL="localhost:9200"

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

if curl $ELASTIC_URL/_cat/indices | grep cities
then
  curl -X DELETE $ELASTIC_URL/cities
fi

# _boost has been removed from 2.0 so removing tihs line:
#   "_boost": {"name" : "city_boost", "null_value" : "1.0"},
#
# See the following page for details and solution if we need
# to reactivate some kind of boosting:
#https://www.elastic.co/guide/en/elasticsearch/reference/1.4/mapping-boost-field.html#function-score-instead-of-boost
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
   "properties" : {
    "name" : { "type" : "string", "analyzer" : "city_name"},
    "zipcode": {"type": "string", "boost": 2.0},
    "name_suggest" : {
     "type" : "completion", "payloads" : true,
     "analyzer": "city_name",
     "preserve_position_increments": false,
     "preserve_separators": false
    }
   }
  }
 }
}'

cat ${install_dir}/cp-france.csv | csv2bulk | bulk_insert
