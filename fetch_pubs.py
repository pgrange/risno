# -*- coding: iso-8859-15 -*-

import hashlib
import urllib2
import re
import random

from bs4 import BeautifulSoup

log_context = ""
def log(status, message = ""):
  from colorama import Fore, Back, Style
  if status == "OK": color = Fore.GREEN
  elif status == "KO": color = Fore.RED
  else: color = Fore.YELLOW
 
  print color + status + " " + Fore.BLUE + log_context + Fore.RESET + " " + message

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP

  for pub in pubs: conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

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

def fetch_page(location, helper):
  return helper.fetch_page(location)


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

  parser.add_argument('locations', nargs=argparse.REMAINDER, help='code postaux où recherche les annones')
  args = parser.parse_args()
  
  sites = []

  from sites_helper import LogicImmo
  from sites_helper import LeBonCoin
  from sites_helper import ParuVendu
  from sites_helper import SeLoger
  from sites_helper import AVendreALouer
  from sites_helper import PagesJaunes
  from sites_helper import ImmoStreet
  
  if args.logic_immo: sites.append(LogicImmo())
  if args.le_bon_coin: sites.append(LeBonCoin())
  if args.paru_vendu: sites.append(ParuVendu())
  if args.se_loger: sites.append(SeLoger())
  if args.avendre_alouer: sites.append(AVendreALouer())
  if args.pages_jaunes: sites.append(PagesJaunes())
  if args.immo_street: sites.append(ImmoStreet())
  
  for site in sites:
    for location in args.locations:
      try:
        log_context = location + ' ' + site.name
        page = fetch_page(location, site)
        pubs = parse(page, site)
	if len(pubs) == 0:
	  log("WA", "no pub, we may have been blacklisted")
        if args.test: show_pubs(pubs)
        else: insert_to_db(pubs)
        log("OK")
      except:
        log("KO", traceback.format_exc())
