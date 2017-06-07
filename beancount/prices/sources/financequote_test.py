__copyright__ = "Copyright (C) 2015-2016  Martin Blais"
__license__ = "GNU GPLv2"

import textwrap
import datetime
import unittest
from unittest import mock
from urllib import error
import subprocess

from beancount.prices.sources import financequote
from beancount.core.number import D
from beancount.core.number import Decimal


class FinanceQuotePriceFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = financequote.Source()

    def test_get_latest_price(self):
        subprocess.check_output = mock.MagicMock(return_value = b'{"GB00B3X7QG63\u001ctime":"17:00","GB00B3X7QG63\u001ccurrency":"GBP","GB00B3X7QG63\u001cname":"Vanguard FTSE U.K. All Share Index Unit Trust Accumulation","GB00B3X7QG63\u001cnav":"194.77","GB00B3X7QG63\u001cisodate":"2017-06-06","GB00B3X7QG63\u001cnet":"0.4069","GB00B3X7QG63\u001csource":"http://funds.ft.com/UK/Tearsheet/Summary?s=GB00B3X7QG63","GB00B3X7QG63\u001clast":"194.77","GB00B3X7QG63\u001cerrormsg":"Warning - failed to find a time","GB00B3X7QG63\u001cprice":"194.77","GB00B3X7QG63\u001csymbol":"GB00B3X7QG63","GB00B3X7QG63\u001csuccess":1,"GB00B3X7QG63\u001cdate":"06/06/2017","GB00B3X7QG63\u001cmethod":"ftfunds","GB00B3X7QG63\u001cp_change":"0.21"}')
        srcprice = self.fetcher.get_latest_price('ftfunds:GB00B3X7QG63')
        self.assertTrue(isinstance(srcprice.price, Decimal))
        self.assertEqual(D('194.77'), srcprice.price)

        subprocess.check_output = mock.MagicMock(return_value = b'{"GOOG\u001cpe":"33.00","GOOG\u001cday_range":"975.14 - 988.25","GOOG\u001cex_div":null,"GOOG\u001cvolume":"1815200","GOOG\u001ctime":"16:00","GOOG\u001cyear_range":"663.28 - 988.25","GOOG\u001cmethod":"yahoo","GOOG\u001csymbol":"GOOG","GOOG\u001cclose":"983.68","GOOG\u001cbid":"975.80","GOOG\u001chigh":"988.25","GOOG\u001cisodate":"2017-06-06","GOOG\u001clast":"976.57","GOOG\u001cask":"985.50","GOOG\u001cdiv_yield":null,"GOOG\u001cdiv_date":null,"GOOG\u001cp_change":"-0.72","GOOG\u001cavg_vol":"1453360","GOOG\u001ccurrency":"USD","GOOG\u001cdiv":null,"GOOG\u001clow":"975.14","GOOG\u001cname":"Alphabet Inc.","GOOG\u001cprice":"976.57","GOOG\u001cnet":"-7.11","GOOG\u001csuccess":"1","GOOG\u001ccap":"675540000000","GOOG\u001ceps":"29.59","GOOG\u001cdate":"06/06/2017","GOOG\u001copen":"983.16"}')
        srcprice = self.fetcher.get_latest_price('nasdaq:GOOG')
        self.assertTrue(isinstance(srcprice.price, Decimal))
        self.assertEqual(D('976.57'), srcprice.price)

    def test_get_latest_price__invalid(self):
        subprocess.check_output = mock.MagicMock(return_value = b'{"HOOG\u001cpe":null,"HOOG\u001cask":null,"HOOG\u001cp_change":null,"HOOG\u001csuccess":"0","HOOG\u001clast":null,"HOOG\u001cyear_range":null,"HOOG\u001cex_div":null,"HOOG\u001ccap":null,"HOOG\u001cbid":null,"HOOG\u001csymbol":"HOOG","HOOG\u001cname":null,"HOOG\u001cvolume":null,"HOOG\u001cdate":null,"HOOG\u001copen":null,"HOOG\u001cclose":null,"HOOG\u001ceps":null,"HOOG\u001cerrormsg":"Stock lookup failed","HOOG\u001cdiv_date":null,"HOOG\u001cnet":null,"HOOG\u001cavg_vol":null,"HOOG\u001ctime":null,"HOOG\u001cdiv":null,"HOOG\u001cdiv_yield":null,"HOOG\u001ccurrency":null,"HOOG\u001cday_range":null}')
        srcprice = self.fetcher.get_latest_price('nasdaq:HOOG')
        self.assertIsNone(srcprice)
