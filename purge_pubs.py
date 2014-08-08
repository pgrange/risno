# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, TermQuery, TextQuery, MatchAllQuery, FilteredQuery, BoolQuery, exceptions
from pyes.filters import NotFilter, HasChildFilter, MissingFilter, TermFilter, ORFilter, MatchAllFilter

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

def check_index_version():
  q = TermQuery('dtc', 'dtc')
  conn.search(query=q, indices=e_index, doc_types="dtc").total

def delete_from_db(pub):
  conn.delete(e_index, "immo", pub.get_id())

def get_pubs():
  q = TermQuery('expired', 'true')
  f = NotFilter(HasChildFilter('opinion', TermQuery('opinion', 'like')))
  q = FilteredQuery(q, f)
  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

if __name__ == '__main__':
  import traceback
  import argparse
  
  log_context = "purge"
  
  parser = argparse.ArgumentParser(description='Supprime les annonces expirées que plus personne ne référence')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces correspondates sans les supprimer')

  args = parser.parse_args()
  
  if not args.test: check_index_version()

  previous_total = -1
  total = 0
  while previous_total != total:
    # That's odd but it seems we do not update all
    # found pubs... so adding this while loop :(
    previous_total = total
    pubs = get_pubs()

    count = 0
    purged = 0
    total = pubs.total
    log('OK', str(total) + ' pubs to purge')
    for pub in pubs:
      if args.test: show_pub(pub)
      else: 
        try:
          delete_from_db(pub)
        except exceptions.NotFoundException:
          log('WA', 'element already suppresed')
      purged = purged + 1
      if purged % 20 == 0:
        log('OK', str(purged) + ' / ' + str(total) + ' purged')
  log('OK', str(purged) + ' pubs purged')
