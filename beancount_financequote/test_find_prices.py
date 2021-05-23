"""Tests for price finding routines.
"""
__copyright__ = "Copyright (C) 2015-2016  Martin Blais"
__license__ = "GNU GPLv2"

import datetime
import types
import unittest

from beancount.ops import find_prices
from beancount.prices import price
from beancount.prices.price import PriceSource as PS
import beancount_financequote
from beancount import loader


class TestImportSource(unittest.TestCase):
    def test_import_source_valid(self):
        for name in ["beancount_financequote"]:
            module = price.import_source(name)
            self.assertIsInstance(module, types.ModuleType)
        module = price.import_source("beancount_financequote")
        self.assertIsInstance(module, types.ModuleType)


class TestParseSource(unittest.TestCase):
    def test_source_valid(self):
        psource = price.parse_single_source("beancount_financequote/NASDAQ:AAPL")
        self.assertEqual(PS(beancount_financequote, "NASDAQ:AAPL", False), psource)


class TestParseSourceMap(unittest.TestCase):
    def _clean_source_map(self, smap):
        return {
            currency: [PS(s[0].__name__, s[1], s[2]) for s in sources]
            for currency, sources in smap.items()
        }

    def test_source_map_onecur_single(self):
        smap = price.parse_source_map("USD:beancount_financequote/NASDAQ:AAPL")
        self.assertEqual(
            {
                "USD": [
                    PS(
                        "beancount_financequote",
                        "NASDAQ:AAPL",
                        False,
                    ),
                ]
            },
            self._clean_source_map(smap),
        )

    def test_source_map_inverse(self):
        smap = price.parse_source_map(
            "USD:beancount_financequote/^CURRENCY:GBPUSD,google/^CURRENCY:GBPUSD"
        )
        self.assertEqual(
            {
                "USD": [
                    PS("beancount_financequote", "CURRENCY:GBPUSD", invert=True),
                    PS(module="google", symbol="CURRENCY:GBPUSD", invert=True),
                ]
            },
            self._clean_source_map(smap),
        )
