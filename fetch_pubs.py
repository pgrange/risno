# -*- coding: iso-8859-15 -*-

import hashlib
import urllib2
import re

from bs4 import BeautifulSoup

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP
  
  for pub in pubs: conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

def image_to_id(image_url):
   return hashlib.md5(urllib2.urlopen(image_url).read()).hexdigest()

class LogicImmo:
  
  def __init__(self):
    self.name = 'logic-immo'
    self.logic_crap = {
      '33114': ('le-barp', '16559_2'),
      '33125': ('toutes-communes', '1525_98'),
      '33650': ('toutes-communes', '1569_98'),
      '33720': ('toutes-communes', '1575_98'),
      '33730': ('toutes-communes', '1576_98'),
      '33770': ('salles', '30867_2'),
      '33830': ('toutes-communes', '1581_98'),
      '40160': ('toutes-communes', '1887_98'),
      '40210': ('toutes-communes', '1892_98'),
      '40410': ('toutes-communes', '1910_98'),
      '40460': ('sanguinet', '30974_2'),
      '33830': ('toutes-communes', '1581_98'),
      '33380': ('toutes-communes', '1548_98'),
      '33160': ('toutes-communes', '1531_98'),
      '33980': ('audenge', '1556_2'),
      '33480': ('toutes-communes', '1557_98'),
      '33680': ('toutes-communes', '1572_98'),
      '33138': ('lanton', '16199_2'),
      '33740': ('ares', '1079_2'),
      '33950': ('toutes-communes', '1588_98'),
      '33970': ('cap-ferret', '36653_2'),
      '33510': ('andernos-les-bains', '726_2')
    }

  def parse(self, page):
    soup = BeautifulSoup(page)
    
    pubs = []
    for div in soup.find_all('div', 'v7_li-ad-global'):
      price = div.find('p', 'v7_li-ad-price').get_text().strip()
      url = div.find('a', href=re.compile("^http://www.logic-immo.com/detail-vente-")).attrs[u'href']
      img = div.find('img').attrs[u'src']
      placement = div.find('p', 'v7_li-ad-loc').get_text().strip()
  
      pubs.append(
        { #'id': '2-' + re.search("(?<=detail-vente-)[^.]+", url).group(0),
          'id': image_to_id(img),
          'object': 
            { 'url': url, 
              'img': img,
              'placement': placement,
              'price': price}})
    
    return pubs

  def search_url(self, location):
    if not self.logic_crap.has_key(location): raise Exception("I do not know this location sorry: " + location)
    crap = self.logic_crap[location]
    return "http://www.logic-immo.com/vente-immobilier-" + crap[0] + "-" + location + "," + crap[1] + "-4f2f000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html"

class LeBonCoin:
  
  def __init__(self):
    self.name = 'le-bon-coin'

  def parse(self, page):
    soup = BeautifulSoup(page)
    
    pubs = []
    for a in soup.find_all('a', href=re.compile("^http://www.leboncoin.fr/ventes_immobilieres/[0-9]+")):
      href = a.attrs[u'href']
      img = a.find('img')
      placement = a.find(class_="placement")
      price = a.find(class_="price")

      if (not href or not img or not placement or not price):
        continue
      img = img.attrs[u'src']

      pubs.append(
        { #'id': '1-' + re.search("(?<=ventes_immobilieres/)[0-9]+", href).group(0),
          'id': image_to_id(img),
          'object': 
            { 'url': href, 
              'img': img,
              'placement': placement.get_text().replace('\n', '').replace(' ', ''),
              'price': price.get_text().strip()}})
    
    return pubs

  def search_url(self, location): 
    return "http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&ret=5&pe=8&location=" + location

class ParuVendu:

  def __init__(self):
    self.name = 'paru-vendu'

  def parse(self, page):
    soup = BeautifulSoup(page)
    
    pubs = []
    for div in soup.find_all('div', 'lazyload_bloc annonce'):
      href = "http://www.paruvendu.fr" + div.find('a').attrs[u'href']
      img = div.find('span', 'img').find('img')
      if img.has_attr('src'): img = img.attrs['src']
      else: img = img.attrs['original']

      placement = div.find('cite')
      price = div.find('span', "price")

      pubs.append(
        { #'id': '1-' + re.search("(?<=ventes_immobilieres/)[0-9]+", href).group(0),
          'id': image_to_id(img),
          'object': 
            { 'url': href, 
              'img': img,
              'placement': placement.get_text().replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', ''),
              'price': price.get_text().strip()}})
    
    return pubs

  def search_url(self, location):
    return "http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=" + location

class SeLoger:

  def __init__(self):
    self.name = 'se-loger'

  def parse(self, page):
    soup = BeautifulSoup(page)
    
    pubs = []
    for div in soup.find_all('div', "ann_ann"):
      href = div.find('a', href=re.compile("http://www.seloger.com/annonces/achat/"))
      if (not href): continue
      href = href.attrs[u'href']
      img = div.find('img').attrs[u'src']
      if (img.startswith('/')): img = "http://www.seloger.com" + img
      placement = div.find('div', 'rech_ville').find('strong').get_text().replace('\n', '').replace('\r', ' ').replace(' ', '')
      price = div.find('span', 'mea2').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
  
      pubs.append(
        { #'id': '2-' + re.search("(?<=/annonces/achat/maison/).*/([0-9]+).htm", href).group(1),
          'id': image_to_id(img),
          'object': 
            { 'url': href, 
              'img': img,
              'placement': placement,
              'price': price}})
    
    return pubs

  def search_url(self, location):
    return "http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&pxmax=200000&tri=d_dt_crea&cp=" + location
 
if __name__ == '__main__':
  import sys
  import argparse
  from colorama import Fore, Back, Style

  parser = argparse.ArgumentParser(description='récupère les annonces pour le site et le code postal précisé')
  parser.add_argument('--le-bon-coin', const=True, action='store_const', help='recherche sur le bon coin')
  parser.add_argument('--logic-immo',  const=True, action='store_const', help='recherche sur logic immo')
  parser.add_argument('--se-loger',    const=True, action='store_const', help='recherche sur se loger')
  parser.add_argument('--paru-vendu',  const=True, action='store_const', help='recherche sur paru vendu')
  parser.add_argument('locations', nargs=argparse.REMAINDER, help='code postaux où recherche les annones')
  args = parser.parse_args()
  
  sites = []
  
  if args.logic_immo: sites.append(LogicImmo())
  if args.le_bon_coin: sites.append(LeBonCoin())
  if args.paru_vendu: sites.append(ParuVendu())
  if args.se_loger: sites.append(SeLoger())
  
  for site in sites:
    for location in args.locations:
      try:
        fetch_info = ' ' + location + ' ' + site.name
        url = site.search_url(location)
        pubs = site.parse(urllib2.urlopen(url))
        insert_to_db(pubs)
        print Fore.GREEN + 'OK' + Fore.RESET + fetch_info
      except:
        e = sys.exc_info()[0]
        print Fore.RED + 'KO' + Fore.RESET + fetch_info + str(e)
