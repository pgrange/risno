import re

from bs4 import BeautifulSoup

class SiteHelper:
  def __init__(self):
    self.price_class = 'price'

  def _parse_price(self, pub):
    return int(
      re.findall('[0-9]+ *[0-9]*', 
        pub.find(class_=self.price_class).get_text().encode('ascii', 'ignore')
      )[0].replace(' ', '')
    )

  def parse(self, page):
    soup = BeautifulSoup(page)
    pubs = []
    for pub in soup.find_all(class_ = self.pub_class):
      pubs.append({
        'price': self._parse_price(pub)
      })

    return pubs

class LeBonCoin(SiteHelper):

  def __init__(self):
    SiteHelper.__init__(self)
    self.pub_class = 'lbc'

  def url(self, location):
    return 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&ret=5&pe=8&location=' + str(location)

class ParuVendu(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.pub_class = 'annonce'

  def url(self, location):
    return 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=' + str(location)

class SeLoger(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.pub_class = 'ann_ann'
    self.price_class = 'rech_box_prix'

  def url(self, location):
    return 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&pxmax=200000&tri=d_dt_crea&cp=' + str(location)

class AVendreALouer(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.pub_class = 'resultat'
    self.price_class = 'prix'

  def url(self, location):
    return 'http://www.avendrealouer.fr/annonces-immobilieres/vente/appartement+maison/' + str(location) + '+cp/max-300000-euros'

class LogicImmo(SiteHelper):
  def __init__(self):
    SiteHelper.__init__(self)
    self.pub_class = 'offer-block'
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

  def url(self, location):
    location = str(location)
    if not self.logic_crap.has_key(location): 
      raise Exception("I do not know this location sorry: " + location)

    return "http://www.logic-immo.com/vente-immobilier-" \
      + self.logic_crap[location][0] + "-" \
      + location + "," \
      + self.logic_crap[location][1] \
      + "-4f2f000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html"
