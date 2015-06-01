# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, MatchQuery, MatchAllQuery, FilteredQuery, BoolQuery
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
 
  from datetime import datetime
  print color + status + " " + Fore.BLUE + log_context +  ' [' + str(datetime.now()) + ']' + Fore.RESET + " " + message.encode('UTF-8')

def insert_to_db(pub):
  if len(pub['cities']) < 1:
    #Ugly hack to avoid updating ads timestamp when no type found
    return
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

def search_city(text):
  q = BoolQuery(minimum_number_should_match=0)
  q.add_must(MatchQuery('name', normalize_query_string(text)))
  q.add_should(MatchQuery('zipcode', normalize_query_string(text)))
  cities = conn.search(query=q, indices="cities")
  if len(cities) < 1:
    log("KO", text)
  return [city.get_id() for city in cities[:1]]

  return result
 
def search_for_locations(pub):
  if 'location' in pub:
    location = pub['location']
  if 'description' in pub:
    description = pub['description']
  cities = []
  if location:
    cities.extend(search_city(location))
  elif description:
    cities.extend(search_city(description))
  pub['cities'] = list(set(cities))
  if len(pub['cities']) > 1:
    log("DBG", str(pub['cities']))

def get_pubs(filter=MissingFilter('cities')):
  q = FilteredQuery(MatchAllQuery(), filter)

  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

if __name__ == '__main__':
  import traceback
  import argparse

  log_context = "upd_location"

  parser = argparse.ArgumentParser(description='met à jour le lieux des annonces en base')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces mises à jour sans les stocker en base')
  parser.add_argument('--all', const=True, action='store_const', help='met à jour toutes les annonces, et pas seulement celles associées à aucune ville')
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
      search_for_locations(pub)
      if args.test: show_pub(pub)
      else: insert_to_db(pub)
      count = count + 1
      if count % 20 == 0:
        log('OK', str(count) + ' / ' + str(total) + ' updated')
