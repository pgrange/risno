import urllib2
def parse_se_loger(page):
  import re
  from bs4 import BeautifulSoup
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

def insert_to_db(pubs):
  from pyes import ES
  conn = ES('127.0.0.1:9200') # Use HTTP
  
  for pub in pubs: conn.update("test-index", "test-type", pub['id'], document=pub['object'], upsert=pub['object'])

def image_to_id(image_url):
   import hashlib
   return hashlib.md5(urllib2.urlopen(image_url).read()).hexdigest()

def open_search_url_for_location(location):
  return urllib2.urlopen("http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,12&pxmax=200000&tri=d_dt_crea&cp=" + location)

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Parse le bon coin results')
  parser.add_argument('location', help='location to search pubs for')
  args = parser.parse_args()

  insert_to_db(parse_se_loger(open_search_url_for_location(args.location)))
