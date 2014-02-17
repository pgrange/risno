import re
import urllib2

import locale

from datetime import timedelta
from datetime import date
from datetime import datetime
 
from bs4 import BeautifulSoup

class SiteHelper:
  def __init__(self):
    self.pub_class = None
    self.pub_tag = None
    self.price_class = None
    self.description_class = None
    self.location_class = None
    self.date_class = None
    self.date_format = '%d/%m/%Y'
    self.date_regex = '[0-9]{2}/[0-9]{2}/[0-9]{4}'

  def _text(self, tag):
    text = tag.get_text() 
    return re.sub("\s+", " ", text).strip()
 
  def _parse_price(self, pub):
    price_block = pub.find(class_=self.price_class)
    if price_block:
      matched = re.findall('[0-9]+ *[0-9]*', 
        price_block.\
          get_text().encode('ascii', 'ignore')
      )
      if len(matched) > 0:
        return int(matched[0].replace(' ', ''))

  def _parse_description(self, pub):
    description = \
      self._text(pub.find(class_=self.description_class))

    if len(description) > 200: return description[:200] + "..."
    else:                      return description

  def _parse_url(self, pub):
    # the whole pub is encapsulated in a link
    # as for le bon coin, for instance
    parent = pub.parent
    if parent.name == 'a':
      return pub.parent['href']

    # the pub link is contained inside the pub.
    # in almost all cases, it is the first link
    # with a non empty href
    pub_url = pub.find('a', href=lambda(x): x != None)['href']
    if pub_url.startswith('http://'):
      return pub_url
    else:
      return 'http://' + self.site + pub_url

    # if none of the above cases matches for your 
    # case, redefine this method in your subclass

  def _parse_img(self, pub):
    img = pub.find('img')
    if img:
      src = img['src']
      if src.startswith('http://'):
        return src
      elif src.startswith('/'):
        return 'http://' + self.site + src

  def _parse_location(self, pub):
    if self.location_class:
      return self._text(pub.find(class_ = self.location_class))

  def _parse_date(self, pub):
    if self.date_class == None:
      return
    s_date = self._text(pub.find(class_ = self.date_class))
    if s_date.startswith('Hier'):
      return date.today() - timedelta(days=1)
    elif s_date.startswith('Aujourd'):
      return date.today()
    if s_date.startswith('Il y a 2 jours'):
      return date.today() - timedelta(days=2)
    if s_date.startswith('Il y a 3 jours'):
      return date.today() - timedelta(days=3)
    if s_date.startswith('Il y a 4 jours'):
      return date.today() - timedelta(days=4)
    if s_date.startswith('Il y a 5 jours'):
      return date.today() - timedelta(days=5)
    if s_date.startswith('Il y a 6 jours'):
      return date.today() - timedelta(days=6)
    if s_date.startswith('Il y a une semaine'):
      return date.today() - timedelta(days=7)
    else:
      if len(re.findall(self.date_regex, s_date)) == 0:
        print s_date
      s_date = re.findall(self.date_regex, s_date)[0].encode('utf8', 'ignore')
      return datetime.strptime(s_date, self.date_format).date()

  def fetch_page(self, location, num_page=1):
    s_url = self.url(location, num_page)
    return urllib2.urlopen(s_url)
    
  def url(self, location, num_page=1):
    """
    Define this method to return the appropriate url
    to get pubs for a given location for this site.

    The pubs should be ordered by publication date.

    location is of the form {'type': <type>, 'id': id},
    type is the type of location and can be either
    'zip' or 'region', 'id' is the id of the location,
    dependding on the type it could be 'aquitaine'
    when type is 'region' or '33125' when type is 'zip'.
    
    num_page is the number of the page to fetch. By default,
    this should be set to 1.

    You can also directly override zip_url and region_url
    instead.
    """
    if location['type'] == 'zip':
      return self.zip_url(location['id'], num_page)
    elif location['type'] == 'region':
      return self.region_url(location['id'], num_page)
    else:
      raise Exception("Illegal type, should be one of 'id' or 'region': " + location['type'])

  def zip_url(self, zip, num_page):
    """
    Define this method to return the appropriate url
    to get pubs for a given zip code for this site and
    the given page.

    The pubs should be ordered by publication date.
    """
    pass

  def region_url(self, region, num_page):
    """
    Define this method to return the appropriate url
    to get pubs for a given region for this site and
    the given page.

    The pubs should be ordered by publication date.
    """
    pass

  def parse(self, page):
    soup = BeautifulSoup(page)
    pubs = []
    for pub in soup.find_all(self.pub_tag, class_ = self.pub_class):
      pubs.append({
        'price': self._parse_price(pub),
        'description': self._parse_description(pub),
        'url': self._parse_url(pub),
        'img': self._parse_img(pub),
        'location': self._parse_location(pub),
        'date': self._parse_date(pub),
      })

    return pubs

class LeBonCoin(SiteHelper):

  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'le-bon-coin'
    self.site = 'leboncoin.fr'
    self.pub_class = 'lbc'
    self.price_class = 'price'
    self.description_class = 'title'
    self.location_class = 'placement'
    self.date_class = 'date'
    self.date_format = '%d %b %H:%M'
    self.date_regex = '.*'

  def _parse_date(self, pub):
    s_date = self._text(pub.find(class_ = self.date_class))
    if s_date.startswith('Hier'):
      return date.today() - timedelta(days=1)
    elif s_date.startswith('Aujourd'):
      return date.today()
    else:
      s_date = re.findall(self.date_regex, s_date)[0].encode('utf8', 'ignore')
      
      # it seems like le bon coin is using a custom
      # date localisation/conversion scheme :(
      # so filtering before parsing
      s_date = re.sub(u'c([^.a-z]|$)', u'c. '.encode('utf8'), s_date)
      s_date = re.sub(u'nov([^.]|$)', u'nov. ', s_date)
      s_date = re.sub(u'oct([^.]|$)', u'oct. ', s_date)
      s_date = re.sub(u'jan([^v][^.]|$)', u'janv. ', s_date)

      old_locale = locale.getlocale(locale.LC_TIME)
      locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
      d = datetime.strptime(s_date, self.date_format).date()
      locale.setlocale(locale.LC_TIME, old_locale)

      if d.year == 1900:
        # no year specified in pub, using current year
        return date(d.today().year, d.month, d.day)
      else:
        return d

  def zip_url(self, location, num_page):
    return 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?location=' + str(location) + '&o=' + str(num_page)

  def region_url(self, region, num_page):
    return 'http://www.leboncoin.fr/ventes_immobilieres/offres/' + region + '/?o=' + str(num_page)

class ParuVendu(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'paru-vendu'
    self.site = 'www.paruvendu.fr'
    self.pub_class = 'annonce'
    self.price_class = 'price'
    self.description_class = 'desc'
    self.date_class = 'date'

  def _parse_img(self, pub):
    img = pub.find('img', original=lambda(x): x != None)
    if img: return img['original']

  def zip_url(self, location, num_page):
    return 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&pa=FR&lo=' + str(location) + '&p=' + str(num_page)

  def region_url(self, region, num_page):
    dept = {'aquitaine': '24,33,40,47,64'}
    return 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&pa=FR&lo=' + dept[region] + '&p=' + str(num_page)

class SeLoger(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'se-loger'
    self.site = 'seloger.com'
    self.pub_class = 'annonce'
    self.pub_tag = 'article'
    self.price_class = 'annonce__agence__prix'
    self.description_class = 'annone__description__small'
    self.location_class = 'annone__detail__localisation'
    #no date displayed know :(
    #self.date_class = 'rech_majref'

  def _parse_location(self, pub):
    return self._text(pub.find(class_ = self.location_class))

  def zip_url(self, location, num_page):
    return 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&tri=d_dt_crea&cp=' + str(location) + '&ANNONCEpg=' + str(num_page)

  def region_url(self, region, num_page):
    id = {'aquitaine': '2229'}
    return 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=1,10,11,12,13,14,2,4,9&tri=d_dt_crea&div=' + id[region] + '&ANNONCEpg=' + str(num_page)

class AVendreALouer(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'a-vendre-a-louer'
    self.site = 'avendrealouer.fr'
    self.pub_class = 'resultat'
    self.price_class = 'prix'
    self.description_class = 'descriptif'
    self.location_class = "annonce_url"
    self.date_class = 'parution'

  def _parse_location(self, pub):
    return self._text(pub.find(class_ = self.location_class))

  def zip_url(self, location, num_page):
    return 'http://www.avendrealouer.fr/annonces-immobilieres/vente/appartement+maison/' + str(location) + '+cp/page-' + str(num_page)

  def region_url(self, region, num_page):
    dept = {'aquitaine': 'dordogne+24+gironde+33+pyrenees-atlantiques+64+landes+40+lot-et-garonne+47'}
    return 'http://www.avendrealouer.fr/annonces-immobilieres/vente/maison/' + dept[region] + '/page-' + str(num_page)

class LogicImmo(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'logic-immo'
    self.site = 'www.logic-immo.com'
    self.pub_class = 'offer-block'
    self.price_class = 'price'
    self.description_class = 'offer-desc'
    self.location_class = 'offer-loc'
    self.date_class = 'offer-updatedate'

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
      '33510': ('andernos-les-bains', '726_2'),
      '33400': ('talence', '32468_2')
    }

  def _parse_location(self, pub):
    return self._text(pub.find(class_ = self.location_class))

  def zip_url(self, location, num_page):
    location = str(location)
    if not self.logic_crap.has_key(location): 
      raise Exception("I do not know this location sorry: " + location)

    return "http://www.logic-immo.com/vente-immobilier-" \
      + self.logic_crap[location][0] + "-" \
      + location + "," \
      + self.logic_crap[location][1] \
      + '-4f2f000000-0,0-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-' + str(num_page) + '.html'

  def region_url(self, region, num_page):
    region_conversion = {'aquitaine': 'aquitaine-33000,15'}
    return 'http://www.logic-immo.com/vente-immobilier-' + region_conversion[region] + '_0-ef2f800000-0,0-0,0-0,0-00-00-000000000000-00-0-0-1-1-0-' + str(num_page) + '.html'

from cookielib import CookieJar
class PagesJaunes(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'pages-jaunes'
    self.site = 'pagesjaunes.fr'
    self.pub_class = 'visitCardContent'
    self.price_class = 'price'
    self.description_class = 'dataCard'
    self.location_class = 'location'
    self.date_class = 'update'

  def _parse_url(self, pub):
    pj_crap = pub.find('a', 'idTag_PARTAGER')['data-pjonglet']
    return "http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do" + re.findall('.*(\?idAnnonce=.*)\'', pj_crap)[0]
    
  def zip_url(self, zip):
    return 'http://www.pagesjaunes.fr/verticales/immo/rechercher.do?transactionSimple=achat&ou=' + zip

  def region_url(self, region):
    return 'http://www.pagesjaunes.fr/verticales/immo/rechercherPA.do?transactionSimple=achat&typeBien=&ou=' + region

  def fetch_page(self, location, num_page=1):
    #they did it again http://ploum.net/ploum-en-j2ee/
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # first get the search page

    if location['type'] == 'zip':
      s_url = self.zip_url(location['id'])
    elif location['type'] == 'region':
      s_url = self.region_url(location['id'])
    else:
      raise Exception("Illegal type, should be one of 'id' or 'region': " + location['type'])

    opener.open(s_url)

    # then sort by date
    opener.open('http://www.pagesjaunes.fr/verticales/immo/trierListeReponses.do?valeurTriImmo=DATE_PUBLICATION')

    # and finally get the correct page (omg !)
    return opener.open('http://www.pagesjaunes.fr/verticales/immo/changerPageListeReponses.do?numPage=' + str(num_page))

class ImmoStreet(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'immo-street'
    self.site = 'www.immostreet.fr'
    self.pub_class = 'item'
    self.price_class = 'price_item'
    self.description_class = 'title_item'
    self.date_class = 'ref_item'
    
    self.immo_street_crap = {
      '33114': 'place_id=4815975',
      '33125': 'place_id=4816379&place_id=4816147&place_id=4816197&place_id=4816477',
      '33650': 'place_id=4816219&place_id=4816442&place_id=4816416&place_id=4816023&place_id=4816397',
      '33720': 'place_id=4816272&place_id=4815976&place_id=4816171&place_id=4816065&place_id=481615&place_id=4816493&place_id=4816022&place_id=4816395&place_id=4816142',
      '33730': 'place_id=4816252&place_id=4816281&place_id=4816488&place_id=4816478&place_id=4815972&place_id=4816274',
      '33770': 'place_id=4816439',
      '33830': 'place_id=4815987',
      '40160': 'place_id=4816734&place_id=4816850&place_id=4816625',
      '40210': 'place_id=4816651&place_id=4816611&place_id=4816821&place_id=4816602&place_id=4816680',
      '40410': 'place_id=4816744&place_id=4816813&place_id=4816717&place_id=4816673&place_id=4816549&place_id=4816688&place_id=4816758',
      '40460': 'place_id=4816805',
      '33830': 'place_id=4815987&place_id=4815988&place_id=4816206',
      '33380': 'place_id=4815997&place_id=4816229&place_id=4816496&place_id=4816498&place_id=4816505',
      '33160': 'place_id=4816392&place_id=4816319&place_id=4816436',
      '33980': 'place_id=4815965',
      '33480': 'place_id=4816050&place_id=4816194&place_id=4816360&place_id=4815968&place_id=4816242&place_id=4816016',
      '33680': 'place_id=4816159&place_id=4816278&place_id=4816469&place_id=4816444&place_id=4816497',
      '33138': 'place_id=4816175',
      '33740': 'place_id=4815956',
      '33950': 'place_id=4816182',
      '33970': 'place_id=4816517',
      '33510': 'place_id=4815950',
      '33400': 'place_id=4816463'
    }

  def zip_url(self, location, num_page=1):
    location = str(location)
    if not self.immo_street_crap.has_key(location): 
      raise Exception("I do not know this location sorry: " + location)

    return "http://www.immostreet.fr/Listing/Search?search_type=3&" \
      + self.immo_street_crap[location] + '&page=' + str(num_page - 1)

  def region_url(self, region, num_page):
    region_conversion = {'aquitaine': 'place_id=4815370'}
    return "http://www.immostreet.fr/Listing/Search?search_type=3&" \
      + region_conversion[region] + '&page=' + str(num_page - 1)

class BelleImmobilier(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'belle-immobilier'
    self.site = 'www.belle-immobilier.fr'
    self.pub_class = 'item'
    self.price_class = 'price'
    self.description_class = 'item-text'
    self.location_class = 'item-title'
    
  def _url(self, num_page=1):
    return 'http://www.belle-immobilier.fr/fr/biens-immobiliers/?order_by=created_at&order_direction=DESC&page=' + str(num_page)

  def zip_url(self, location, num_page=1):
    return self._url(num_page)

  def region_url(self, region, num_page):
    return self._url(num_page)
