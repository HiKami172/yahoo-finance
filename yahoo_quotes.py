#!/usr/bin/python3
import sys

import fire
from yahooquery import Ticker
from datetime import datetime
import pytz
from pprint import pprint


def get_quotes(*symbols):
    """
    Retrieves and formats quotes for specified stock symbols.

    This function takes one or more stock symbols as arguments, retrieves the quotes for these symbols, formats the quotes, and prints the formatted quotes.

    Args:
        *symbols (str): One or more stock symbols.

    Returns:
        dict: A dictionary where the keys are the stock symbols and the values are dictionaries containing the formatted quotes for each symbol.

    Raises:
        Exception: If there is an error retrieving or formatting the quotes.
    """
    data = Ticker(list(symbols))
    quotes = data.quotes
    if not isinstance(quotes, dict):
        print("Error while retrieving quotes.", file=sys.stderr)
        sys.exit(1)

    def extract_attrs(quote):
        format_time = lambda unix_time, tz_code: datetime.fromtimestamp(unix_time, pytz.timezone(tz_code))
        tz_code = quote['exchangeTimezoneShortName']
        try:
            regular_market_time = format_time(quote['regularMarketTime'], tz_code)
            regular_market_open = format_time(quote['regularMarketOpen'], tz_code)
            first_trade_time = format_time(quote['firstTradeDateMilliseconds'] / 1000, tz_code)
        except Exception as e:
            print(f"Error converting to market time: {e}")
        return {
            'regularMarketPrice': quote['regularMarketPrice'],
            'firstTradeDateMilliseconds': first_trade_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'regularMarketTime': regular_market_time.strftime('%I:%M%p %Z'),
            'regularMarketOpen': regular_market_open.strftime('%I:%M%p %Z'),
            'regularMarketDayHigh': quote['regularMarketDayHigh'],
            'regularMarketDayLow': quote['regularMarketDayLow'],
            'regularMarketVolume': quote['regularMarketVolume'],
            'bid': quote['bid'],
            'ask': quote['ask'],
        }
    try:
        result = {k: extract_attrs(v) for k, v in quotes.items()}
    except KeyError as e:
        print(f"Error while extracting quotes data: {e}\n"
              "Review symbols string and try again.")
        sys.exit(1)
    pprint(result)


if __name__ == '__main__':
    fire.Fire({
        'get_quotes': get_quotes
    })
