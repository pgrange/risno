#!/bin/bash

index="immo2"

#curl -XDELETE localhost:9200/${index}

curl -XPUT localhost:9200/${index} -d '
{
 "mappings": {
  "immo": {
   "properties": {
    "url": {"index": "not_analyzed", "type": "string"},
    "img": {"index": "not_analyzed", "type": "string"},
    "location": {"type": "string"},
    "description": {"type": "string"},
    "cities": {"type": "string"},
    "price": {"type": "integer"},
    "date": {"type": "date"}
   }
  },
  "opinion" : {
   "_parent": {"type": "immo"},
   "properties": {
    "user_code" : { "type" : "string"},
    "opinion": {"type": "string"}
   }
  }
 }
}'

# TO REMOVE
curl -X POST localhost:9200/${index}/immo/1 -d '
{
 "url": "http://example.com/test1",
 "img": "http://example.com/test1",
 "location": "test1",
 "description": "cool",
 "price": 200000
}'
curl -X POST localhost:9200/${index}/immo/2 -d '
{
 "url": "http://example.com/test2",
 "img": "http://example.com/test2",
 "location": "test2",
 "description": "super cool",
 "price": 200001
}'
curl -X POST localhost:9200/${index}/immo/3 -d '
{
 "url": "http://example.com/test3",
 "img": "http://example.com/test3",
 "location": "test3",
 "description": "super méga cool",
 "price": 200002
}'
