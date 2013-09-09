def parse_le_bon_coin(page):
  import re
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(page)
  
  pubs = []
  for a in soup.find_all('a', href=re.compile("^http://www.leboncoin.fr/ventes_immobilieres/[0-9]+")):
    href = a.attrs[u'href']
    img = a.find('img')
    placement = a.find(class_="placement")
    price = a.find(class_="price")

    if (not href or not img or not placement or not price):
      continue

    pubs.append(
      { 'id': '1-' + re.search("(?<=ventes_immobilieres/)[0-9]+", href).group(0),
        'object': 
          { 'url': href, 
            'img': img.attrs[u'src'],
            'placement': placement.get_text().replace('\n', '').replace(' ', ''),
            'price': price.get_text().strip()}})
  
  return pubs

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP
  
  for pub in pubs: conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

def open_search_url_for_location(location):
  import urllib2
  return urllib2.urlopen("http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&pe=8&location=" + location)

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Parse le bon coin results')
  parser.add_argument('location', help='location to search pubs for')
  args = parser.parse_args()

  
  insert_to_db(parse_le_bon_coin(open_search_url_for_location(args.location)))
