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
          { 'id': re.search("(?<=ventes_immobilieres/)[0-9]+", href).group(0), 
            'url': href, 
            'img': img.attrs[u'src'],
            'placement': placement.get_text().replace('\n', '').replace(' ', ''),
            'price': price.get_text().strip()})
  
  return pubs

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Parse le bon coin results')
  parser.add_argument('location', help='location to search pubs for')
  args = parser.parse_args()

  import urllib2
  page = urllib2.urlopen("http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=1&ret=1&location=" + args.location)
  print page.url
  print parse_le_bon_coin(page)
