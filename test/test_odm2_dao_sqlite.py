from __future__ import (absolute_import, division, print_function)

import os
import unittest

from wof.examples.flask.odm2.timeseries.odm2_timeseries_dao import Odm2Dao as OdmDao  # noqa

ODM2_DATABASE_URI = 'sqlite:///' + "./test/odm2/ODM2.sqlite"
ODM2_ONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    'test_odm2_sqlite.cfg'
)


class TestOdmDao(unittest.TestCase):
    def setUp(self):
        self.dao = OdmDao(ODM2_DATABASE_URI)
        self.known_site_codes = [
            'USU-LBR-Mendon'
        ]

        self.fake_codes = [
            'junk',
            'trash',
            'fake'
        ]

        self.known_var_codes = [
            'USU36'
        ]

        self.known_series = [
            ('USU-LBR-Mendon', 'USU36', '2007-08-16 23:30:00.000', '2008-03-27 19:30:00.000')  # noqa
        ]

        self.known_bbox = {
            'west': -114,
            'south': 40,
            'east': -110,
            'north': 42
        }

    def test_get_all_sites(self):
        siteResultList = self.dao.get_all_sites()
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_site_codes:
            self.assertTrue(known_code in resultSiteCodes)

    def test_get_site_by_code(self):
        for known_code in self.known_site_codes:
            siteResult = self.dao.get_site_by_code(known_code)
            self.assertEqual(known_code, siteResult.SiteCode)

    def test_get_sites_by_codes(self):
        siteResultList = self.dao.get_sites_by_codes(self.known_site_codes)
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_site_codes:
            self.assertTrue(known_code in resultSiteCodes)

    def test_get_sites_by_box(self):
        siteResultList = self.dao.get_sites_by_box(self.known_bbox['west'],
                                                   self.known_bbox['south'],
                                                   self.known_bbox['east'],
                                                   self.known_bbox['north'])
        resultSiteCodes = [s.SiteCode for s in siteResultList]
        for known_code in self.known_site_codes:
            self.assertTrue(known_code in resultSiteCodes)

    def test_get_all_variables(self):
        varResultList = self.dao.get_all_variables()
        resultVarCodes = [v.VariableCode for v in varResultList]
        for known_code in self.known_var_codes:
            self.assertTrue(known_code in resultVarCodes)

    def test_get_var_by_code(self):
        for known_code in self.known_var_codes:
            varResult = self.dao.get_variable_by_code(known_code)
            self.assertEqual(known_code, varResult.VariableCode)

    def test_get_vars_by_codes(self):
        varResultList = self.dao.get_variables_by_codes(self.known_var_codes)
        resultVarCodes = [v.VariableCode for v in varResultList]
        for known_code in self.known_var_codes:
            self.assertTrue(known_code in resultVarCodes)
