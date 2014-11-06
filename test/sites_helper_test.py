# -*- coding: utf-8 -*-
import unittest

import sites_helper

class TestSitesHelper(unittest.TestCase):

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

import os
_dir_ = os.path.dirname(__file__)

if __name__ == '__main__':
  unittest.main()
