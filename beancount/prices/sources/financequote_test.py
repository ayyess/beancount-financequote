__copyright__ = "Copyright (C) 2015-2016  Martin Blais"
__license__ = "GNU GPLv2"

import textwrap
import datetime
import unittest
from unittest import mock
from urllib import error
import subprocess

from beancount.prices.sources import finance_quote
from beancount.core.number import D
from beancount.core.number import Decimal


class FinanceQuotePriceFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = finance_quote.Source()

    def test_get_latest_price(self):
        subprocess.check_output = mock.MagicMock(return_value = b'GBP,06/02/2017,195.88\r\n')
        srcprice = self.fetcher.get_latest_price('ftfunds/GB00B3X7QG63')
        self.assertTrue(isinstance(srcprice.price, Decimal))
        self.assertEqual(D('195.88'), srcprice.price)

        srcprice = self.fetcher.get_latest_price('mstaruk/GB00B3X7QG63')
        self.assertTrue(isinstance(srcprice.price, Decimal))
        self.assertEqual(D('195.88'), srcprice.price)
