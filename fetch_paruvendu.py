import urllib2

def parse_paruvendu(page):
  import re
  from bs4 import BeautifulSoup
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

def image_to_id(image_url):
   import hashlib
   return hashlib.md5(urllib2.urlopen(image_url).read()).hexdigest()

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP
  
  for pub in pubs: 
    conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

def open_search_url_for_location(location):
  return urllib2.urlopen("http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=" + location)

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Parse le bon coin results')
  parser.add_argument('location', help='location to search pubs for')
  args = parser.parse_args()

  
  insert_to_db(parse_paruvendu(open_search_url_for_location(args.location)))
