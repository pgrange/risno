# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, MatchQuery, TermQuery, TextQuery, MatchAllQuery, FilteredQuery, BoolQuery, ESRange
from pyes.filters import MissingFilter, TermFilter, ORFilter, MatchAllFilter, RangeFilter
from datetime import datetime, timedelta

elastic_url=os.environ.get('ELASTIC_URL', '127.0.0.1:9200')
conn = ES(elastic_url) # Use HTTP
e_index = "ads_2.2"

log_context = ""
def log(status, message = ""):
  from colorama import Fore, Back, Style
  if status == "OK": color = Fore.GREEN
  elif status == "KO": color = Fore.RED
  else: color = Fore.YELLOW
 
  from datetime import datetime
  print color + status + " " + Fore.BLUE + log_context +  ' [' + str(datetime.now()) + ']' + Fore.RESET + " " + message.encode('UTF-8')

def check_index_version():
  q = TermQuery('dtc', 'dtc')
  conn.search(query=q, indices=e_index, doc_types="dtc").total

def insert_to_db(pub):
  conn.update(e_index, "immo", pub.get_id(), document=pub, upsert=pub)

def get_to_expire_pubs(site, last_fetch):
  q = TermQuery('site_name', site)
  q = FilteredQuery(q, MissingFilter('expired'))
  q = FilteredQuery(q, RangeFilter(qrange=ESRange('_timestamp', to_value=last_fetch)))

  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

def expired_before_timestamp(site):
  twentyfour_hours_ago = int((datetime.now()-timedelta(days=1)).strftime("%s"))*1000
  return twentyfour_hours_ago
  #q = MatchQuery('site', site)
  #fetch_info = conn.search(query=q, indices='utils', doc_types="fetch_info", sort='last_fetch:desc')
  #if len(fetch_info) > 0: return fetch_info[0]['last_fetch']
  ##FIXME this is the future bug of 2038 january the 19th 3:14:7
  #return 21474836470

def expire(pub):
  pub['expired'] = True

if __name__ == '__main__':
  import traceback
  import argparse

  log_context = "expire"

  parser = argparse.ArgumentParser(description='Détecte et marque en base les annonces périmée (dernière récupération il y a plus de 24h)')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces mises à jour sans les stocker en base')
  parser.add_argument('--le-bon-coin', const=True, action='store_const', help='recherche sur le bon coin')
  parser.add_argument('--logic-immo',  const=True, action='store_const', help='recherche sur logic immo')
  parser.add_argument('--se-loger',    const=True, action='store_const', help='recherche sur se loger')
  parser.add_argument('--paru-vendu',  const=True, action='store_const', help='recherche sur paru vendu')
  parser.add_argument('--avendre-alouer',  const=True, action='store_const', help='recherche sur à vendre à louer')
  parser.add_argument('--pages-jaunes',  const=True, action='store_const', help='recherche sur pages jaunes')
  parser.add_argument('--annonces-jaunes',  const=True, action='store_const', help='recherche sur annonces jaunes')
  parser.add_argument('--immo-street',  const=True, action='store_const', help='recherche sur immo street')
  parser.add_argument('--belle-immobilier',  const=True, action='store_const', help='recherche sur belle-immobilier.fr')

  args = parser.parse_args()
  
  if not args.test: check_index_version()

  sites = []

  if args.logic_immo: sites.append('logic-immo')
  if args.le_bon_coin: sites.append('le-bon-coin')
  if args.paru_vendu: sites.append('paru-vendu')
  if args.se_loger: sites.append('se-loger')
  if args.avendre_alouer: sites.append('a-vendre-a-louer')
  if args.pages_jaunes: sites.append('pages-jaunes')
  if args.annonces_jaunes: sites.append('annonces-jaunes')
  if args.immo_street: sites.append('immo-street')
  if args.belle_immobilier: sites.append('belle-immobilier')

  for site in sites:
    previous_total = -1
    total = 0
    while previous_total != total:
      # That's odd but it seems we do not update all
      # found pubs... so adding this while loop :(
      previous_total = total

      pubs = get_to_expire_pubs(site, expired_before_timestamp(site))

      count = 0
      expired = 0
      total = pubs.total
      log('OK', str(total) + ' pubs to expire')
      for pub in pubs:
        expire(pub)
        expired = expired + 1
        if args.test: show_pub(pub)
        else: insert_to_db(pub)
        count = count + 1
        if count % 20 == 0:
          log('OK', str(count) + ' / ' + str(total) + ' updated')
    log('OK', str(expired) + ' pubs expired for ' + site)
