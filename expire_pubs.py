# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, TermQuery, TextQuery, MatchAllQuery, FilteredQuery, BoolQuery
from pyes.filters import MissingFilter, TermFilter, ORFilter, MatchAllFilter

elastic_url=os.environ.get('ELASTIC_URL', '127.0.0.1:9200')
conn = ES(elastic_url) # Use HTTP
e_index = "ads_2.1"

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

def insert_to_db(pub):
  conn.update(e_index, "immo", pub.get_id(), document=pub, upsert=pub)

def get_pubs(site):
  q = TermQuery('site_name', site.name)
  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

def expire(pub, site):
  return True

if __name__ == '__main__':
  import traceback
  import argparse

  parser = argparse.ArgumentParser(description='Détecte et marque en base les annonces périmée')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces mises à jour sans les stocker en base')
  parser.add_argument('--le-bon-coin', const=True, action='store_const', help='recherche sur le bon coin')
  parser.add_argument('--logic-immo',  const=True, action='store_const', help='recherche sur logic immo')
  parser.add_argument('--se-loger',    const=True, action='store_const', help='recherche sur se loger')
  parser.add_argument('--paru-vendu',  const=True, action='store_const', help='recherche sur paru vendu')
  parser.add_argument('--avendre-alouer',  const=True, action='store_const', help='recherche sur à vendre à louer')
  parser.add_argument('--pages-jaunes',  const=True, action='store_const', help='recherche sur pages jaunes')
  parser.add_argument('--immo-street',  const=True, action='store_const', help='recherche sur immo street')
  parser.add_argument('--belle-immobilier',  const=True, action='store_const', help='recherche sur belle-immobilier.fr')

  args = parser.parse_args()
  
  if not args.test: check_index_version()

  sites = []

  from sites_helper import LogicImmo
  from sites_helper import LeBonCoin
  from sites_helper import ParuVendu
  from sites_helper import SeLoger
  from sites_helper import AVendreALouer
  from sites_helper import PagesJaunes
  from sites_helper import ImmoStreet
  from sites_helper import BelleImmobilier
  
  if args.logic_immo: sites.append(LogicImmo())
  if args.le_bon_coin: sites.append(LeBonCoin())
  if args.paru_vendu: sites.append(ParuVendu())
  if args.se_loger: sites.append(SeLoger())
  if args.avendre_alouer: sites.append(AVendreALouer())
  if args.pages_jaunes: sites.append(PagesJaunes())
  if args.immo_street: sites.append(ImmoStreet())
  if args.belle_immobilier: sites.append(BelleImmobilier())

  for site in sites:
    previous_total = -1
    total = 0
    while previous_total != total:
      # That's odd but it seems we do not update all
      # found pubs... so adding this while loop :(
      previous_total = total
      pubs = get_pubs(site)

      count = 0
      expired = 0
      total = pubs.total
      log('OK', str(total) + ' pubs to update')
      for pub in pubs:
        if expire(pub, site):
          expired = expired + 1
          if args.test: show_pub(pub)
          else: insert_to_db(pub)
        count = count + 1
        if count % 20 == 0:
          log('OK', str(count) + ' / ' + str(total) + ' updated')
    log('OK', str(expired) + ' pubs expired for ' + site.name)
