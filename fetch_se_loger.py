import urllib2
def parse_le_bon_coin(page):
  import re
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(page)
  
  pubs = []
  for div in soup.find_all('div', "ann_ann"):
    href = div.find('a', href=re.compile("http://www.seloger.com/annonces/achat/")).attrs[u'href']
    img = div.find('img').attrs[u'src']
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

def open_search_url_for_location():
  return urllib2.urlopen("http://www.seloger.com/recherche.htm?pxbtw=NaN/NaN&surfacebtw=NaN/NaN&idtt=2&nb_pieces=all&idtypebien=2,12&bilance=all&bilanegs=all&=&nb_chambres=all&tri=d_dt_crea&ci=330029,330042,330077,330197,330202,330251,330260,330336,330436,330498,330501,400032,400134,400156,400200,400227,400287,400295,400332&idqfix=1&BCLANNpg=1")

if __name__ == '__main__':
  
  insert_to_db(parse_le_bon_coin(open_search_url_for_location()))
