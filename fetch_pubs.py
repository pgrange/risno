# -*- coding: iso-8859-15 -*-

import hashlib
import urllib2
import re
import random

from bs4 import BeautifulSoup

from pyes import ES, TermQuery
conn = ES('127.0.0.1:9200') # Use HTTP
e_index = "ads_2.0"

log_context = ""
def log(status, message = ""):
  from colorama import Fore, Back, Style
  if status == "OK": color = Fore.GREEN
  elif status == "KO": color = Fore.RED
  else: color = Fore.YELLOW
 
  print color + status + " " + Fore.BLUE + log_context + Fore.RESET + " " + message

def check_index_version():
  q = TermQuery('dtc', 'dtc')
  conn.search(query=q, indices=e_index, doc_types="dtc").total

def insert_to_db(pubs):
  for pub in pubs: 
    conn.update(e_index, "immo", pub['id'], document=pub['object'], upsert=pub['object'])

def show_pubs(pubs):
  for pub in pubs:
    print pub

def image_to_id(image_url):
   try:
     return str(hashlib.md5(urllib2.urlopen(image_url).read()).hexdigest())
   except urllib2.URLError as err:
     log("WA", "Unable to generate id from image, generating from image url instead: " + str(err.reason))
     return "default-" + hashlib.md5(image_url).hexdigest()
   except ValueError as err:
     log("WA", "Unable to generate id from image, generating from image url instead: " + str(err))
     return "default-" + hashlib.md5(image_url).hexdigest()

def parse(page, helper):
  return \
    [{'id':  image_to_id(o['img']), 'object': o} 
     for o in helper.parse(page) if o['img'] != None]

def fetch_page(location, helper, num_page):
  return helper.fetch_page(location, num_page)


if __name__ == '__main__':
  import traceback
  import argparse

  parser = argparse.ArgumentParser(description='récupère les annonces pour le site et le code postal précisé')
  parser.add_argument('--test', const=True, action='store_const', help='affiche les annonces sans les stocker en base')
  parser.add_argument('--le-bon-coin', const=True, action='store_const', help='recherche sur le bon coin')
  parser.add_argument('--logic-immo',  const=True, action='store_const', help='recherche sur logic immo')
  parser.add_argument('--se-loger',    const=True, action='store_const', help='recherche sur se loger')
  parser.add_argument('--paru-vendu',  const=True, action='store_const', help='recherche sur paru vendu')
  parser.add_argument('--avendre-alouer',  const=True, action='store_const', help='recherche sur à vendre à louer')
  parser.add_argument('--pages-jaunes',  const=True, action='store_const', help='recherche sur pages jaunes')
  parser.add_argument('--immo-street',  const=True, action='store_const', help='recherche sur immo street')
  parser.add_argument('--belle-immobilier',  const=True, action='store_const', help='recherche sur belle-immobilier.fr')

  parser.add_argument('--zip', metavar='<zipcode>', nargs='*', help='liste des codes postaux des annonces à récupérer')
  parser.add_argument('--region', metavar='<region>', nargs='*', help='liste des régions des annonces à récupérer (seul aquitaine est supporté pour le moment)')

  parser.add_argument('--max-pages', action='store', help="ne récupère pas plus de <max-pages> pages sur chaque site, quoiqu'il arrive. Par défaut 200", type=int, default=200)

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

  locations = {}
  for site in sites:
    locations[site] = []
    if args.zip:
      locations[site].extend([{'type': 'zip', 'id': zip} for zip in args.zip])
    if args.region:
      locations[site].extend([{'type': 'region', 'id': region} for region in args.region])

  num_page = 1
  while (len(sites) > 0 and num_page <= args.max_pages):
    site_i = 0
    while site_i < len(sites):
      site = sites[site_i]
      locations_i = 0
      while locations_i < len(locations[site]):
        location = locations[site][locations_i]
        try:
          log_context = location['id'] + '/' + str(num_page) + ' ' + site.name
          page = fetch_page(location, site, num_page)
          pubs = parse(page, site)
          if len(pubs) == 0:
            if (num_page == 0):
              log("WA", "no pub, we may have been blacklisted")
            else:
              log('OK', 'all pages fetched, removing this locations for this site')
              locations[site].remove(location)
              locations_i = locations_i - 1
              if len(locations[site]) == 0:
                log('OK', 'no more locations for the site, removing this site')
                sites.remove(site) 
                site_i = site_i - 1
          if args.test: show_pubs(pubs)
          else: insert_to_db(pubs)
          log("OK")
        except:
          log("KO", traceback.format_exc())
        
        locations_i = locations_i + 1

      site_i = site_i + 1

    num_page = num_page + 1
