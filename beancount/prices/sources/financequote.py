"""Fetch prices using Perl's Finance::Quote module.
"""
__copyright__ = "Copyright (C) 2015-2016  Martin Blais"
__license__ = "GNU GPLv2"

import datetime
import os
import subprocess

from beancount.core.number import D
from beancount.prices import source
from beancount.utils import net_utils


class Source(source.Source):
    "Fetch prices using Perl's Finance::Quote module."

    def get_latest_price(self, ticker_pair):
        """See contract in beancount.prices.source.Source."""

        path_to_script = os.path.abspath(os.path.dirname(__file__)) + "/financequote.pl"
        params = [path_to_script]

        # ticker_pair is a string in the form "module:ticker"
        params.extend(ticker_pair.split(':', 1))
        if len(params) != 3:
            return None  # module and ticker were not both supplied

        # financequote.pl's output is in the form b"currency,date,price"
        output = subprocess.check_output(params)

        pricing = output.decode("utf-8").split(',')
        if not pricing[0]:
            return None  # data was not able to be fetched

        currency = pricing[0]
        # Finance::Quote returns date in mm/dd/YY format
        trade_date = datetime.datetime.strptime(pricing[1], "%m/%d/%Y")
        price = D(pricing[2])
        return source.SourcePrice(price, trade_date, currency)

    def get_historical_price(self, ticker, date):
        """See contract in beancount.prices.source.Source."""
        return None
