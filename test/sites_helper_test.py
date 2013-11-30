# -*- coding: utf-8 -*-
import unittest

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

  def test_parse_sites_extracts_every_pub(self):
    self.assertEquals(11, len(self._parse_le_bon_coin()))
    self.assertEquals(3, len(self._parse_paru_vendu()))
    self.assertEquals(9, len(self._parse_logic_immo()))
    self.assertEquals(7, len(self._parse_se_loger()))
    self.assertEquals(12, len(self._parse_a_vendre_a_louer()))

  def test_parse_sites_extracts_price(self):
    self.assertEquals(155850, self._parse_le_bon_coin()[0]['price'])
    self.assertEquals(187000, self._parse_paru_vendu()[0]['price'])
    self.assertEquals(96500, self._parse_logic_immo()[0]['price'])
    self.assertEquals(149000, self._parse_se_loger()[0]['price'])
    self.assertEquals(178500, self._parse_a_vendre_a_louer()[0]['price'])

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

  def test_parse_site_extract_date(self):
    from datetime import date
    from datetime import timedelta
    self.assertEquals(date.today()-timedelta(1), 
                      self._parse_le_bon_coin()[0]['date'])
    self.assertEquals(date(2013, 11, 13), 
                      self._parse_le_bon_coin()[2]['date'])
    #self.assertEquals(None, 
    #                  self._parse_paru_vendu()[0]['location'])
    #self.assertEquals(_logic_immo_test_location, 
    #                  self._parse_logic_immo()[0]['location'])
    #self.assertEquals(_se_loger_test_location, 
    #                  self._parse_se_loger()[0]['location'])
    #self.assertEquals(_a_vendre_a_louer_test_location, 
    #                  self._parse_a_vendre_a_louer()[0]['location'])



  def _parse_le_bon_coin(self):
    return self._parse(sites_helper.LeBonCoin(), _le_bon_coin_test_page_)

  def _parse_paru_vendu(self):
    return self._parse(sites_helper.ParuVendu(), _paru_vendu_test_page_)

  def _parse_logic_immo(self):
    return self._parse(sites_helper.LogicImmo(), _logic_immo_test_page_)

  def _parse_se_loger(self):
    return self._parse(sites_helper.SeLoger(), _se_loger_test_page_)

  def _parse_a_vendre_a_louer(self):
    return self._parse(sites_helper.AVendreALouer(), _a_vendre_a_louer_test_page_)

  def _parse(self, helper, test_page):
    page = open(test_page)
    result = helper.parse(page)
    page.close()

    return result

import os
_dir_ = os.path.dirname(__file__)
_le_bon_coin_test_page_ = os.path.join(_dir_, 'le_bon_coin_test_page.html')
_paru_vendu_test_page_  = os.path.join(_dir_, 'paru_vendu_test_page.html')
_logic_immo_test_page_  = os.path.join(_dir_, 'logic_immo_test_page.html')
_se_loger_test_page_    = os.path.join(_dir_, 'se_loger_test_page.html')
_a_vendre_a_louer_test_page_ = os.path.join(_dir_, 'a_vendre_a_louer_test_page.html')

_le_bon_coin_33400_url = 'http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?sp=0&ret=1&ret=5&pe=8&location=33400'
_paru_vendu_33400_url  = 'http://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=1&tbMai=1&tbVil=1&tbCha=1&tbPro=1&tbHot=1&tbMou=1&tbFer=1&tbPen=1&tbRem=1&tbVia=1&tbImm=1&tbPar=1&tbAut=1&px1=200000&pa=FR&lo=33400'
_logic_immo_33400_url  = 'http://www.logic-immo.com/vente-immobilier-talence-33400,32468_2-4f2f000000-0,200000-0,0-0,0-00-00-000000000000-00-0-0-3-0-0-1.html'
_se_loger_33400_url    = 'http://www.seloger.com/recherche.htm?idtt=2&idtypebien=2,10,12,11,9,13,14&pxmax=200000&tri=d_dt_crea&cp=33400'
_a_vendre_a_louer_33400_url = 'http://www.avendrealouer.fr/annonces-immobilieres/vente/appartement+maison/33400+cp/max-300000-euros'

_le_bon_coin_test_description_ = u'Maison 3 pièces 64m2'
_paru_vendu_test_description_  = u'Vente - Maison - 55 m² environ - 2 pièces Talence (33400) Maison en pierre de 2 pièces principalesMaison en pierre de plain pied... voir l\'annonce'
_logic_immo_test_description_ = u'TALENCE (33400) Achat maison Talence - Talence proche bagatelle atelier d\'environ 50m² à restaurer. SQUARE HABITAT T\xe9l. 0556041899 R\xe9f. annonce : 107950-1231'
_se_loger_test_description_ = u'33400 Talence (Gironde) Proximité: Boulevards TALENCE Proche Boulevard - Maison T4 à rénover de 79m² dont 71m² carrez comprenant 3 chambres et une terrasse de 15m². Elle est idéalement placée à 2 pas ...'
_a_vendre_a_louer_test_description = u'Se situant à Talence, appartement T5 de 84m2, agréable à vivre, proche des commodités, comporte 3 chambres bien tenues, u...'

_le_bon_coin_test_url = u'http://www.leboncoin.fr/ventes_immobilieres/570168457.htm?ca=2_s'
_paru_vendu_test_url = u'http://www.paruvendu.fr/immobilier/vente/maison/talence-33400/1188107770A1KIVHMN000'
_logic_immo_test_url =u'http://www.logic-immo.com/detail-vente-76c1da9a-d5bc-3d28-ee27-6731eb81bd88.htm' 
_se_loger_test_url =u'http://www.seloger.com/annonces/achat/maison/talence-33/83022761.htm?cp=33400&idtt=2&idtypebien=10,11,12,13,14,2,9&pxmax=200000&tri=d_dt_crea' 
_a_vendre_a_louer_test_url ='http://www.avendrealouer.fr/annonces-immobilieres/48/vente+appartement+5-pieces+talence+33/detail+pro-13056540/' 

_le_bon_coin_test_img = u'http://193.164.197.40/thumbs/247/247316102112100.jpg' 
_paru_vendu_test_img = u'http://media.paruvendu.fr/media_ext/9927/21/20/th/th_992721200800_1.jpg' 
_logic_immo_test_img = u'http://mmf.logic-immo.com/mmf/ads/photo-prop-182x136/76c/c/c543e6fa-1231-4c1c-98a4-0158c1a7dcc4.jpg' 
_se_loger_test_img = u'/z/produits/sl/sv6_gen/images/ssPhoto.gif' 
_a_vendre_a_louer_test_img = u'http://img1.avendrealouer.fr/photos_pro/12554/proa13056540.jpg?lastmodified='

_le_bon_coin_test_location = u'Talence / Gironde'
_logic_immo_test_location = u'TALENCE (33400)'
_se_loger_test_location = u'33400 Talence (Gironde) Proximité: Boulevards'
_a_vendre_a_louer_test_location = u'Vente Appartement 5 pièces 84 m² 33400 TALENCE'

if __name__ == '__main__':
  unittest.main()
