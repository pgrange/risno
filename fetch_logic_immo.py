logic_crap = {
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
}

def parse_logic_immo(page):
  import re
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(page)
  
  pubs = []
  for div in soup.find_all('div', 'v7_li-ad-global'):
    price = div.find('p', 'v7_li-ad-price').get_text().strip()
    url = div.find('a', href=re.compile("^http://www.logic-immo.com/detail-vente-")).attrs[u'href']
    img = div.find('img').attrs[u'src']
    placement = div.find('p', 'v7_li-ad-loc').get_text().strip()

    pubs.append(
      { 'id': '2-' + re.search("(?<=detail-vente-)[^.]+", url).group(0),
        'object': 
          { 'url': url, 
            'img': img,
            'placement': placement,
            'price': price}})
  
  return pubs

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP
  
  for pub in pubs: conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

def open_search_url_for_location(location):
  import urllib2
  crap = logic_crap[location]
  if not crap: raise Exception("I do not know this location sorry: " + location)
  return urllib2.urlopen("http://www.logic-immo.com/vente-immobilier-" 
    + crap[0] + "-" + location + "," + crap[1] 
    + "-420e000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html")

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Parse le bon coin results')
  parser.add_argument('location', help='location to search pubs for')
  args = parser.parse_args()

  
  insert_to_db(parse_logic_immo(open_search_url_for_location(args.location)))
