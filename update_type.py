# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, TextQuery, MatchAllQuery, FilteredQuery, BoolQuery
from pyes.filters import MissingFilter, TermFilter, ORFilter, MatchAllFilter

elastic_url=os.environ.get('ELASTIC_URL', '127.0.0.1:9200')
conn = ES(elastic_url) # Use HTTP
e_index = "ads"

log_context = ""
def log(status, message = ""):
  from colorama import Fore, Back, Style
  if status == "OK": color = Fore.GREEN
  elif status == "KO": color = Fore.RED
  else: color = Fore.YELLOW
 
  print color + status + " " + Fore.BLUE + log_context + Fore.RESET + " " + message.encode('UTF-8')

def insert_to_db(pub):
  conn.update(e_index, "immo", pub.get_id(), document=pub, upsert=pub)

def normalize_query_string(query_string):
  return query_string\
    .replace('/', ' ')\
    .replace('"', ' ')\
    .replace('!', ' ')\
    .replace('~', ' ')\
    .replace(':', ' ')\
    .replace('(', ' ')\
    .replace(')', ' ')

def search_type(text):
  q = BoolQuery(minimum_number_should_match=0)
  #TODO add synonyms instead of relying on 'french'
  q.add_must(TextQuery('french', normalize_query_string(text)))
  types = conn.search(query=q, indices="types")
  if len(types) < 1:
    log("KO", text)
  return [t.get_id() for t in types[:1]]

  return result
 
def search_for_types(pub):
  location = pub['location']
  description = pub['description']
  text = description
  if location: text = text + " " + location
  types = []
  types.extend(search_type(text))
  pub['types'] = list(set(types))
  if len(pub['types']) > 1:
    log("DBG", str(pub['types']))

def get_pubs(filter=MissingFilter('types')):
  q = FilteredQuery(MatchAllQuery(), filter)

  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

if __name__ == '__main__':
  import traceback
  import argparse

 log_context = "upd_type"

  parser = argparse.ArgumentParser(description='met à jour le type des annonces en base')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces mises à jour sans les stocker en base')
  parser.add_argument('--all', const=True, action='store_const', help='met à jour toutes les annonces, et pas seulement celles associées à aucun type')
  parser.add_argument('--term', action='store', help='met à jour uniquement les annonces correspondant au terme précisé')

  args = parser.parse_args()
  
  previous_total = -1
  total = 0
  while previous_total != total:
    # That's odd but it seems we do not update all
    # found pubs... so adding this while loop :(
    previous_total = total
    if args.all: pubs = get_pubs(filter=MatchAllFilter())
    elif args.term: 
      filter=ORFilter([TermFilter(field="description", value=args.term),
                       TermFilter(field="location", value=args.term)])
      pubs = get_pubs(filter=filter)
    else: pubs = get_pubs()

    count = 0
    total = pubs.total
    log('OK', str(total) + ' pubs to update')
    for pub in pubs:
      search_for_types(pub)
      if args.test: show_pub(pub)
      else: insert_to_db(pub)
      count = count + 1
      if count % 20 == 0:
        log('OK', str(count) + ' / ' + str(total) + ' updated')
