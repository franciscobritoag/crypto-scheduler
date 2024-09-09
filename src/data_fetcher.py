from pycoingecko import CoinGeckoAPI
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Fetch historical cryptocurrency price data using the CoinGecko API.
# :param symbol: The symbol of the cryptocurrency (e.g., 'bitcoin').
# :param vs_currency: The currency to compare against (e.g., 'usd').
# :param days: The number of past days to fetch (e.g., '365' for 1 year).
# :return: A DataFrame with historical price data.
def get_crypto_data(symbol, vs_currency='usd', days='365'):
    cg = CoinGeckoAPI()
    try:
        data = cg.get_coin_market_chart_by_id(id=symbol, vs_currency=vs_currency, days=days)
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None
