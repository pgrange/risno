# -*- coding: utf-8 -*-
import unittest

from datetime import date
from datetime import timedelta

import sites_helper

class TestSitesHelper(unittest.TestCase):

  def setUp(self):
    self.maxDiff = None

  def test_sites_url(self):
    self.assertEquals(sites_helper.LeBonCoin().url(33400), 
                      _le_bon_coin_33400_url)
    self.assertEquals(sites_helper.ParuVendu().url(33400), 
                      _paru_vendu_33400_url)
    self.assertEquals(sites_helper.LogicImmo().url(33400), 
                      _logic_immo_33400_url)
    self.assertEquals(sites_helper.SeLoger().url(33400), 
                      _se_loger_33400_url)
    self.assertEquals(sites_helper.AVendreALouer().url(33400), 
                      _a_vendre_a_louer_33400_url)
    self.assertEquals(sites_helper.PagesJaunes().url(33400), 
                      _pages_jaunes_33400_url)
    self.assertEquals(sites_helper.ImmoStreet().url(33400), 
                      _immo_street_33400_url)

  def test_parse_sites_extracts_every_pub(self):
    self.assertEquals(11, len(self._parse_le_bon_coin()))
    self.assertEquals(3, len(self._parse_paru_vendu()))
    self.assertEquals(9, len(self._parse_logic_immo()))
    self.assertEquals(8, len(self._parse_se_loger()))
    self.assertEquals(12, len(self._parse_a_vendre_a_louer()))
    self.assertEquals(10, len(self._parse_pages_jaunes()))
    self.assertEquals(10, len(self._parse_immo_street()))

  def test_parse_sites_extracts_price(self):
    self.assertEquals(155850, self._parse_le_bon_coin()[0]['price'])
    self.assertEquals(187000, self._parse_paru_vendu()[0]['price'])
    self.assertEquals(96500, self._parse_logic_immo()[0]['price'])
    self.assertEquals(187000, self._parse_se_loger()[0]['price'])
    self.assertEquals(178500, self._parse_a_vendre_a_louer()[0]['price'])
    self.assertEquals(59000, self._parse_pages_jaunes()[0]['price'])
    self.assertEquals(125000, self._parse_immo_street()[0]['price'])

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

  def test_parse_site_extract_date(self):
    self.assertEquals(date.today()-timedelta(1), 
                      self._parse_le_bon_coin()[0]['date'])
    self.assertEquals(date.today(), 
                      self._parse_le_bon_coin()[1]['date'])
    self.assertEquals(date(2013, 11, 13), 
                      self._parse_le_bon_coin()[3]['date'])
    self.assertEquals(date(2013, 12, 13), 
                      self._parse_le_bon_coin()[2]['date'])

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

    self.assertEquals(date(2013, 7, 19), 
                      self._parse_a_vendre_a_louer()[0]['date'])
    self.assertEquals(date(2013, 10, 10), 
                      self._parse_pages_jaunes()[0]['date'])
    self.assertEquals(date(2013, 9, 17),
                      self._parse_immo_street()[0]['date'])

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

import os
_dir_ = os.path.dirname(__file__)
_le_bon_coin_test_page_ = os.path.join(_dir_, 'le_bon_coin_test_page.html')
_paru_vendu_test_page_  = os.path.join(_dir_, 'paru_vendu_test_page.html')
_logic_immo_test_page_  = os.path.join(_dir_, 'logic_immo_test_page.html')
_se_loger_test_page_    = os.path.join(_dir_, 'se_loger_test_page.html')
_a_vendre_a_louer_test_page_ = os.path.join(_dir_, 'a_vendre_a_louer_test_page.html')
_pages_jaunes_test_page_ = os.path.join(_dir_, 'pages_jaunes_test_page.html')
_immo_street_test_page_ = os.path.join(_dir_, 'immo_street_test_page.html')

_le_bon_coin_33400_url = 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&ret=5&pe=8&location=33400'
_paru_vendu_33400_url  = 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=33400'
_logic_immo_33400_url  = 'http://www.logic-immo.com/vente-immobilier-talence-33400,32468_2-4f2f000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html'
_se_loger_33400_url    = 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&pxmax=200000&tri=d_dt_crea&cp=33400'
_a_vendre_a_louer_33400_url = 'http://www.avendrealouer.fr/annonces-immobilieres/vente/appartement+maison/33400+cp/max-300000-euros'
_pages_jaunes_33400_url = 'http://www.pagesjaunes.fr/verticales/immo/rechercher.do?transactionSimple=achat&ou=33400'
_immo_street_33400_url = u'http://www.immostreet.fr/Listing/Search?search_type=3&place_id=4816463'

_le_bon_coin_test_description_ = u'Maison 3 pièces 64m2'
_paru_vendu_test_description_  = u'Vente - Maison - 55 m² environ - 2 pièces Talence (33400) Maison en pierre de 2 pièces principalesMaison en pierre de plain pied... voir l\'annonce'
_logic_immo_test_description_ = u'TALENCE (33400) Achat maison Talence - Talence proche bagatelle atelier d\'environ 50m² à restaurer. SQUARE HABITAT T\xe9l. 0556041899 R\xe9f. annonce : 107950-1231'
_se_loger_test_description_ = u"Talence M\xe9doquine Maison en pierre \xe0 r\xe9nover de plain-pied d'environ 55 m\xb2 avec jardin bien expos\xe9. Secteur calme, proche de toutes..."
_a_vendre_a_louer_test_description = u'Se situant à Talence, appartement T5 de 84m2, agréable à vivre, proche des commodités, comporte 3 chambres bien tenues, u...'
_pages_jaunes_test_description = u"Dans Bordeaux, Barriere de Toulouse Axe tr\u010ds passant. Grande vitrine. Parking Proche des commerces de proximit\xe9 Bail 3.6.9 tous commerces Local \u0155 visiter Mise \xe0 jour le 10/10/2013 Partager Voir l'anno..."
_immo_street_test_description = u'Vente - Appartement 5 pièces - 83 m2 - Talence'

_le_bon_coin_test_url = u'http://www.leboncoin.fr/ventes_immobilieres/570168457.htm?ca=2_s'
_paru_vendu_test_url = u'http://www.paruvendu.fr/immobilier/vente/maison/talence-33400/1188107770A1KIVHMN000'
_logic_immo_test_url =u'http://www.logic-immo.com/detail-vente-76c1da9a-d5bc-3d28-ee27-6731eb81bd88.htm' 
_se_loger_test_url =u'http://www.seloger.com/annonces/achat/maison/talence-33/medoquine-haut-brion/84241325.htm?cp=33400&idtt=2&idtypebien=10,11,12,13,14,2,9&pxmax=200000&tri=d_dt_crea&bd=Li_LienAnn_1' 
_a_vendre_a_louer_test_url ='http://www.avendrealouer.fr/annonces-immobilieres/48/vente+appartement+5-pieces+talence+33/detail+pro-13056540/' 
_pages_jaunes_test_url = u'http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do?idAnnonce=2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca' 
_immo_street_test_url = u'http://www.immostreet.fr/france/talence-4816463/vente/appartement/appartement-5-pieces-80809999?searchString=c2VjdGlvbk5hbWU9JnNlYXJjaF90eXBlPTMsNSwxMCwxMiZwbGFjZV9pZD00ODE2NDYzJnN1cHBvcnRfaWQ9MTEmaXNfZW5hYmxlZD1UcnVlJnNvcnQ9MiZwYWdlPTA1&current=1&nbResults=140&page_precedent=1' 

_le_bon_coin_test_img = u'http://193.164.197.40/thumbs/247/247316102112100.jpg' 
_paru_vendu_test_img = u'http://media.paruvendu.fr/media_ext/9927/21/20/th/th_992721200800_1.jpg' 
_logic_immo_test_img = u'http://mmf.logic-immo.com/mmf/ads/photo-prop-182x136/76c/c/c543e6fa-1231-4c1c-98a4-0158c1a7dcc4.jpg' 
_se_loger_test_img = u'http://6.visuels.poliris.com/c175/6/b/0/8/6b08bf96-3bf0.jpg' 
_a_vendre_a_louer_test_img = u'http://img1.avendrealouer.fr/photos_pro/12554/proa13056540.jpg?lastmodified='
_pages_jaunes_test_img = u'http://media1.annoncesjaunes.fr/images/annonces/immo//20130123/2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca_af621e43-f1f2-44e3-9e5c-e161f1e12c86/'
_immo_street_test_img = u'http://7.visuels.poliris.com/c175/7/4/0/f/740f7d3b-5fc2.jpg'

_le_bon_coin_test_location = u'Talence / Gironde'
_logic_immo_test_location = u'TALENCE (33400)'
_se_loger_test_location = u'Talence 33400 (Gironde)'
_a_vendre_a_louer_test_location = u'Vente Appartement 5 pièces 84 m² 33400 TALENCE'
_pages_jaunes_test_location = u'Talence (33)'

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

if __name__ == '__main__':
  unittest.main()
