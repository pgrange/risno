# -*- coding: utf-8 -*-
import unittest

from datetime import date
from datetime import timedelta

import sites_helper

class TestSitesHelper(unittest.TestCase):

  def setUp(self):
    self.maxDiff = None

  def test_expired_ads_detected(self):
    self.assert_expired(sites_helper.LeBonCoin(),
                        "expired_le_bon_coin_test_page.html")
    self.assert_not_expired(sites_helper.LeBonCoin(),
                            "not_expired_le_bon_coin_test_page.html")

    self.assert_expired(sites_helper.ParuVendu(),
                        "expired_paru_vendu_test_page.html")
    self.assert_not_expired(sites_helper.ParuVendu(),
                            "not_expired_paru_vendu_test_page.html")

    self.assert_expired(sites_helper.SeLoger(),
                        "expired_se_loger_test_page.html")
    self.assert_not_expired(sites_helper.SeLoger(),
                            "not_expired_se_loger_test_page.html")

    self.assert_expired(sites_helper.AVendreALouer(),
                        "expired_avendre_alouer_test_page.html")
    self.assert_not_expired(sites_helper.AVendreALouer(),
                            "not_expired_avendre_alouer_test_page.html")

    self.assert_expired(sites_helper.LogicImmo(),
                        "expired_logic_immo_test_page.html")
    self.assert_not_expired(sites_helper.LogicImmo(),
                            "not_expired_logic_immo_test_page.html")

    self.assert_expired(sites_helper.PagesJaunes(),
                        "expired_pages_jaunes_test_page.html")
    self.assert_not_expired(sites_helper.PagesJaunes(),
                            "not_expired_pages_jaunes_test_page.html")

    self.assert_expired(sites_helper.ImmoStreet(),
                        "expired_immo_street_test_page.html")
    self.assert_not_expired(sites_helper.ImmoStreet(),
                            "not_expired_immo_street_test_page.html")

    self.assert_expired(sites_helper.BelleImmobilier(),
                        "expired_belle_immobilier_test_page.html")
    self.assert_not_expired(sites_helper.BelleImmobilier(),
                            "not_expired_belle_immobilier_test_page.html")

  def assert_expired(self, helper, page_name):
    self.assertTrue(self.expired(helper, os.path.join(_dir_, page_name)))
  def assert_not_expired(self, helper, page_name):
    self.assertFalse(self.expired(helper, os.path.join(_dir_, page_name)))
  def expired(self, helper, file_name):
    page = open(file_name)
    result = helper._expired(page)
    page.close()
    return result

  def test_sites_url(self):
    _33400 = {'type': 'zip', 'id': 33400}
    self.assertEquals(sites_helper.LeBonCoin().url(_33400), 
                      _le_bon_coin_33400_url)
    self.assertEquals(sites_helper.ParuVendu().url(_33400), 
                      _paru_vendu_33400_url)
    self.assertEquals(sites_helper.LogicImmo().url(_33400), 
                      _logic_immo_33400_url)
    self.assertEquals(sites_helper.SeLoger().url(_33400), 
                      _se_loger_33400_url)
    self.assertEquals(sites_helper.AVendreALouer().url({'type': 'region', 'id': 'aquitaine'}), 
                      _a_vendre_a_louer_aquitaine_url)
    self.assertEquals(sites_helper.ImmoStreet().url(_33400), 
                      _immo_street_33400_url)
    self.assertEquals(sites_helper.BelleImmobilier().url(_33400), 
                      _belle_immobilier_33400_url)

  def test_parse_sites_extracts_every_pub(self):
    self.assertEquals(11, len(self._parse_le_bon_coin()))
    self.assertEquals(3, len(self._parse_paru_vendu()))
    self.assertEquals(9, len(self._parse_logic_immo()))
    self.assertEquals(10, len(self._parse_se_loger()))
    self.assertEquals(20, len(self._parse_a_vendre_a_louer()))
    self.assertEquals(10, len(self._parse_pages_jaunes()))
    self.assertEquals(10, len(self._parse_immo_street()))
    self.assertEquals(10, len(self._parse_belle_immobilier()))

  def test_parse_sites_extracts_price(self):
    self.assertEquals(155850, self._parse_le_bon_coin()[0]['price'])
    self.assertEquals(187000, self._parse_paru_vendu()[0]['price'])
    self.assertEquals(96500, self._parse_logic_immo()[0]['price'])
    self.assertEquals(30, self._parse_se_loger()[0]['price'])
    self.assertEquals(290000, self._parse_a_vendre_a_louer()[0]['price'])
    self.assertEquals(59000, self._parse_pages_jaunes()[0]['price'])
    self.assertEquals(125000, self._parse_immo_street()[0]['price'])
    self.assertEquals(208000, self._parse_belle_immobilier()[0]['price'])

  def test_parse_site_extract_description(self):
    self.assertEquals(_le_bon_coin_test_description_, 
                      self._parse_le_bon_coin()[0]['description'])
    self.assertEquals(_paru_vendu_test_description_, 
                      self._parse_paru_vendu()[0]['description'])
    self.assertEquals(_logic_immo_test_description_, 
                      self._parse_logic_immo()[0]['description'])
    self.assertEquals(_se_loger_test_description_, 
                      self._parse_se_loger()[0]['description'])
    self.assertEquals(_a_vendre_a_louer_test_description, 
                      self._parse_a_vendre_a_louer()[0]['description'])
    self.assertEquals(_pages_jaunes_test_description, 
                      self._parse_pages_jaunes()[0]['description'])
    self.assertEquals(_immo_street_test_description, 
                      self._parse_immo_street()[0]['description'])
    self.assertEquals(_belle_immobilier_test_description, 
                      self._parse_belle_immobilier()[0]['description'])

  def test_parse_site_extract_url(self):
    self.assertEquals(_le_bon_coin_test_url, 
                      self._parse_le_bon_coin()[0]['url'])
    self.assertEquals(_paru_vendu_test_url, 
                      self._parse_paru_vendu()[0]['url'])
    self.assertEquals(_logic_immo_test_url, 
                      self._parse_logic_immo()[0]['url'])
    self.assertEquals(_se_loger_test_url, 
                      self._parse_se_loger()[0]['url'])
    self.assertEquals(_a_vendre_a_louer_test_url, 
                      self._parse_a_vendre_a_louer()[0]['url'])
    self.assertEquals(_pages_jaunes_test_url, 
                      self._parse_pages_jaunes()[0]['url'])
    self.assertEquals(_immo_street_test_url, 
                      self._parse_immo_street()[0]['url'])
    self.assertEquals(_belle_immobilier_test_url, 
                      self._parse_belle_immobilier()[0]['url'])

  def test_parse_site_extract_img(self):
    self.assertEquals(_le_bon_coin_test_img, 
                      self._parse_le_bon_coin()[0]['img'])
    self.assertEquals(_paru_vendu_test_img, 
                      self._parse_paru_vendu()[0]['img'])
    self.assertEquals(_logic_immo_test_img, 
                      self._parse_logic_immo()[0]['img'])
    self.assertEquals(_se_loger_test_img, 
                      self._parse_se_loger()[0]['img'])
    self.assertEquals(_a_vendre_a_louer_test_img, 
                      self._parse_a_vendre_a_louer()[0]['img'])
    self.assertEquals(_pages_jaunes_test_img, 
                      self._parse_pages_jaunes()[0]['img'])
    self.assertEquals(_immo_street_test_img, 
                      self._parse_immo_street()[0]['img'])
    self.assertEquals(_belle_immobilier_test_img, 
                      self._parse_belle_immobilier()[0]['img'])

  def test_parse_site_extract_location(self):
    self.assertEquals(_le_bon_coin_test_location, 
                      self._parse_le_bon_coin()[0]['location'])
    #unable to extract location from paru-vendu
    self.assertEquals(None, 
                      self._parse_paru_vendu()[0]['location'])
    self.assertEquals(_logic_immo_test_location, 
                      self._parse_logic_immo()[0]['location'])
    self.assertEquals(_se_loger_test_location, 
                      self._parse_se_loger()[0]['location'])
    self.assertEquals(_a_vendre_a_louer_test_location, 
                      self._parse_a_vendre_a_louer()[0]['location'])
    self.assertEquals(_pages_jaunes_test_location, 
                      self._parse_pages_jaunes()[0]['location'])
    #unable to extract location from immo-street
    self.assertEquals(None, 
                      self._parse_immo_street()[0]['location'])
    self.assertEquals(_belle_immobilier_test_location, 
                      self._parse_belle_immobilier()[0]['location'])

  def test_parse_site_extract_date(self):
    self.assertEquals(date.today()-timedelta(1), 
                      self._parse_le_bon_coin()[0]['date'])
    self.assertEquals(date.today(), 
                      self._parse_le_bon_coin()[1]['date'])
    self.assertEquals(date(date.today().year, 12, 13), 
                      self._parse_le_bon_coin()[2]['date'])
    self.assertEquals(date(date.today().year, 11, 13), 
                      self._parse_le_bon_coin()[3]['date'])
    self.assertEquals(date(date.today().year, 01, 03), 
                      self._parse_le_bon_coin()[4]['date'])
    self.assertEquals(date(date.today().year, 02, 12), 
                      self._parse_le_bon_coin()[5]['date'])

    self.assertEquals(date.today() - timedelta(7), 
                      self._parse_paru_vendu()[0]['date'])
    self.assertEquals(date(2013, 10, 8), 
                      self._parse_paru_vendu()[1]['date'])
    self.assertEquals(date.today()-timedelta(2), 
                      self._parse_paru_vendu()[2]['date'])

    self.assertEquals(date(2013, 11, 13), 
                      self._parse_logic_immo()[0]['date'])
    # no date on this site
    self.assertEquals(None,
                      self._parse_se_loger()[0]['date'])

    self.assertEquals(date(2014, 8, 16), 
                      self._parse_a_vendre_a_louer()[0]['date'])
    self.assertEquals(date(2013, 10, 10), 
                      self._parse_pages_jaunes()[0]['date'])
    self.assertEquals(date(2013, 9, 17),
                      self._parse_immo_street()[0]['date'])
    # no date on this site
    self.assertEquals(None,
                      self._parse_belle_immobilier()[0]['date'])

  def _parse_le_bon_coin(self):
    return _parsed_le_bon_coin

  def _parse_paru_vendu(self):
    return _parsed_paru_vendu

  def _parse_logic_immo(self):
    return _parsed_logic_immo

  def _parse_se_loger(self):
    return _parsed_se_loger

  def _parse_a_vendre_a_louer(self):
    return _parsed_a_vendre_a_louer

  def _parse_pages_jaunes(self):
    return _parsed_pages_jaunes

  def _parse_immo_street(self):
    return _parsed_immo_street

  def _parse_belle_immobilier(self):
    return _parsed_belle_immobilier

import os
_dir_ = os.path.dirname(__file__)
_le_bon_coin_test_page_ = os.path.join(_dir_, 'le_bon_coin_test_page.html')
_paru_vendu_test_page_  = os.path.join(_dir_, 'paru_vendu_test_page.html')
_logic_immo_test_page_  = os.path.join(_dir_, 'logic_immo_test_page.html')
_se_loger_test_page_    = os.path.join(_dir_, 'se_loger_test_page.html')
_a_vendre_a_louer_test_page_ = os.path.join(_dir_, 'a_vendre_a_louer_test_page.html')
_pages_jaunes_test_page_ = os.path.join(_dir_, 'pages_jaunes_test_page.html')
_immo_street_test_page_ = os.path.join(_dir_, 'immo_street_test_page.html')
_belle_immobilier_test_page_ = os.path.join(_dir_, 'belle_immobilier_test_page.html')

_le_bon_coin_33400_url = 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?location=33400&o=1'
_paru_vendu_33400_url  = 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&pa=FR&lo=33400&p=1'
_logic_immo_33400_url  = 'http://www.logic-immo.com/vente-immobilier-talence-33400,32468_2-4f2f000000-0,0-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html'
_se_loger_33400_url    = 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&tri=d_dt_crea&cp=33400&ANNONCEpg=1'
_a_vendre_a_louer_aquitaine_url = 'http://www.avendrealouer.fr/vente/aquitaine/b-maison/loc-2-72.html?page=1'
_pages_jaunes_33400_url = 'http://www.pagesjaunes.fr/verticales/immo/rechercher.do?transactionSimple=achat&ou=33400'
_immo_street_33400_url = u'http://www.immostreet.fr/Listing/Search?search_type=3&place_id=4816463&page=0'
_belle_immobilier_33400_url = u'http://www.belle-immobilier.fr/fr/biens-immobiliers/?order_by=created_at&order_direction=DESC&page=1'

_le_bon_coin_test_description_ = u'Maison 3 pièces 64m2'
_paru_vendu_test_description_  = u'Vente - Maison - 55 m² environ - 2 pièces Talence (33400) Maison en pierre de 2 pièces principalesMaison en pierre de plain pied... voir l\'annonce'
_logic_immo_test_description_ = u'TALENCE (33400) Achat maison Talence - Talence proche bagatelle atelier d\'environ 50m² à restaurer. SQUARE HABITAT T\xe9l. 0556041899 R\xe9f. annonce : 107950-1231'
_se_loger_test_description_ = u"A Penne d'agenais, \xe0 6 minutes de Villeneuve sur Lot, \xe0 2 minutes des..."
_a_vendre_a_louer_test_description = u'Type : Maison Pi\xe8ces : 7 pi\xe8ces Surface : 170 m\xb2'
_pages_jaunes_test_description = u"Dans Bordeaux, Barriere de Toulouse Axe tr\u010ds passant. Grande vitrine. Parking Proche des commerces de proximit\xe9 Bail 3.6.9 tous commerces Local \u0155 visiter Mise \xe0 jour le 10/10/2013 Partager Voir l'anno..."
_immo_street_test_description = u'Vente - Appartement 5 pièces - 83 m2 - Talence'
_belle_immobilier_test_description = u"Grande maison familiale offrant de grands volumes et de nombreuses pièces à deux pas des commodités. Une dépandance attenante à réhabiliter. Des travaux sont à prévoir dans l'habitation principale !!!..."

_le_bon_coin_test_url = u'http://www.leboncoin.fr/ventes_immobilieres/570168457.htm?ca=2_s'
_paru_vendu_test_url = u'http://www.paruvendu.fr/immobilier/vente/maison/talence-33400/1188107770A1KIVHMN000'
_logic_immo_test_url =u'http://www.logic-immo.com/detail-vente-76c1da9a-d5bc-3d28-ee27-6731eb81bd88.htm' 
_se_loger_test_url =u'http://www.seloger.com/annonces/achat/terrain/penne-d-agenais-47/82041079.htm?div=2229&idtt=2&idtypebien=1,10,11,12,13,14,2,4,9&bd=Li_LienAnn_1' 
_a_vendre_a_louer_test_url ='http://www.avendrealouer.fr/vente/marmande-47/b-maison/7-pieces/loc-101-21266/fd-5953407.html' 
_pages_jaunes_test_url = u'http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do?idAnnonce=2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca' 
_immo_street_test_url = u'http://www.immostreet.fr/france/talence-4816463/vente/appartement/appartement-5-pieces-80809999?searchString=c2VjdGlvbk5hbWU9JnNlYXJjaF90eXBlPTMsNSwxMCwxMiZwbGFjZV9pZD00ODE2NDYzJnN1cHBvcnRfaWQ9MTEmaXNfZW5hYmxlZD1UcnVlJnNvcnQ9MiZwYWdlPTA1&current=1&nbResults=140&page_precedent=1' 
_belle_immobilier_test_url = u'http://www.belle-immobilier.fr/fr/bien-immobilier/a-10-min-de-l-ocean-en-plein-coeur-du-village' 

_le_bon_coin_test_img = u'http://193.164.197.40/thumbs/247/247316102112100.jpg' 
_paru_vendu_test_img = u'http://media.paruvendu.fr/media_ext/9927/21/20/th/th_992721200800_1.jpg' 
_logic_immo_test_img = u'http://mmf.logic-immo.com/mmf/ads/photo-prop-182x136/76c/c/c543e6fa-1231-4c1c-98a4-0158c1a7dcc4.jpg' 
_se_loger_test_img = u'http://8.visuels.poliris.com/c175/8/5/0/0/8500bee5-298c.jpg' 
_a_vendre_a_louer_test_img = u'http://cdn-img1-na.avendrealouer.fr/photos_pro_big/1240/PROa18462231.jpg?preset=l'
_pages_jaunes_test_img = u'http://media1.annoncesjaunes.fr/images/annonces/immo//20130123/2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca_af621e43-f1f2-44e3-9e5c-e161f1e12c86/'
_immo_street_test_img = u'http://7.visuels.poliris.com/c175/7/4/0/f/740f7d3b-5fc2.jpg'
_belle_immobilier_test_img = u'http://www.belle-immobilier.fr/upload/modules/estate_i18n/img/210/min-1.jpg'

_le_bon_coin_test_location = u'Talence / Gironde'
_logic_immo_test_location = u'TALENCE (33400)'
_se_loger_test_location = u'Penne d Agenais'
_a_vendre_a_louer_test_location = u'Marmande (47200)'
_pages_jaunes_test_location = u'Talence (33)'
_belle_immobilier_test_location = u"A 10 MIN DE L'OCEAN, EN PLEIN COEUR DU VILLAGE"

# BeautifulSoup is to slow to parse all the pages
# in every test :(
def _parse(helper, test_page):
  page = open(test_page)
  result = helper.parse(page)
  page.close()

  return result

_parsed_le_bon_coin = \
  _parse(sites_helper.LeBonCoin(), _le_bon_coin_test_page_)
_parsed_paru_vendu = \
  _parse(sites_helper.ParuVendu(), _paru_vendu_test_page_)
_parsed_logic_immo = \
  _parse(sites_helper.LogicImmo(), _logic_immo_test_page_)
_parsed_se_loger = \
  _parse(sites_helper.SeLoger(), _se_loger_test_page_)
_parsed_a_vendre_a_louer = \
  _parse(sites_helper.AVendreALouer(), _a_vendre_a_louer_test_page_)
_parsed_pages_jaunes = \
  _parse(sites_helper.PagesJaunes(), _pages_jaunes_test_page_)
_parsed_immo_street = \
  _parse(sites_helper.ImmoStreet(), _immo_street_test_page_)
_parsed_belle_immobilier = \
  _parse(sites_helper.BelleImmobilier(), _belle_immobilier_test_page_)

if __name__ == '__main__':
  unittest.main()
