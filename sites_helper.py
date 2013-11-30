import re

from bs4 import BeautifulSoup

class SiteHelper:
  def __init__(self):
    self.pub_class = None
    self.price_class = None
    self.description_class = None
    self.location_class = None

  def _text(self, tag):
    text = tag.get_text() 
    return re.sub("\s+", " ", text).strip()
 
  def _parse_price(self, pub):
    return int(
      re.findall('[0-9]+ *[0-9]*', 
        pub.find(class_=self.price_class).\
          get_text().encode('ascii', 'ignore')
      )[0].replace(' ', '')
    )

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
    if img: return img['src']

  def _parse_location(self, pub):
    if self.location_class:
      return self._text(pub.find(class_ = self.location_class))

  def _parse_date(self, date):
    pass

  def url(self, location):
    """
    Define this method to return the appropriate url
    to get pubs for a given location for this site.

    The pubs should be ordered by publication date.
    """
    pass

  def parse(self, page):
    soup = BeautifulSoup(page)
    pubs = []
    for pub in soup.find_all(class_ = self.pub_class):
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
    self.pub_class = 'lbc'
    self.price_class = 'price'
    self.description_class = 'title'
    self.location_class = 'placement'

  def _parse_date(self, pub):
    from datetime import timedelta
    from datetime import date
    from datetime import datetime
    s_date = self._text(pub.find(class_ = "date"))
    if s_date.startswith('Hier'):
      return date.today() - timedelta(days=1)
    elif s_date.startswith('Aujourd'):
      return date.today()
    else:
      d = datetime.strptime(s_date, '%d %b %H:%M')
      return date(date.today().year, d.month, d.day)

  def url(self, location):
    return 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&ret=5&pe=8&location=' + str(location)

class ParuVendu(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'paru-vendu'
    self.site = 'www.paruvendu.fr'
    self.pub_class = 'annonce'
    self.price_class = 'price'
    self.description_class = 'desc'

  def _parse_img(self, pub):
    return pub.find('img', original=lambda(x): x != None)['original']

  def url(self, location):
    return 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=' + str(location)

class SeLoger(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'se-loger'
    self.pub_class = 'ann_ann'
    self.price_class = 'rech_box_prix'
    self.description_class = 'rech_desc_right_photo'
    self.location_class = 'rech_ville'

  def _parse_location(self, pub):
    return self._text(pub.find(class_ = self.location_class))

  def url(self, location):
    return 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&pxmax=200000&tri=d_dt_crea&cp=' + str(location)

class AVendreALouer(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'a-vendre-a-louer'
    self.pub_class = 'resultat'
    self.price_class = 'prix'
    self.description_class = 'descriptif'
    self.location_class = "annonce_url"

  def _parse_location(self, pub):
    return self._text(pub.find(class_ = self.location_class))

  def url(self, location):
    return 'http://www.avendrealouer.fr/annonces-immobilieres/vente/appartement+maison/' + str(location) + '+cp/max-300000-euros'

class LogicImmo(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.name = 'logic-immo'
    self.pub_class = 'offer-block'
    self.price_class = 'price'
    self.description_class = 'offer-desc'
    self.location_class = 'offer-loc'
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

  def url(self, location):
    location = str(location)
    if not self.logic_crap.has_key(location): 
      raise Exception("I do not know this location sorry: " + location)

    return "http://www.logic-immo.com/vente-immobilier-" \
      + self.logic_crap[location][0] + "-" \
      + location + "," \
      + self.logic_crap[location][1] \
      + "-4f2f000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html"
