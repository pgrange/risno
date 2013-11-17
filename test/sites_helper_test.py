import unittest

import sites_helper

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


class TestSitesHelper(unittest.TestCase):

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

if __name__ == '__main__':
  unittest.main()
