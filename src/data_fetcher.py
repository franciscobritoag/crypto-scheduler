from pycoingecko import CoinGeckoAPI
import pandas as pd
import logging
import requests

logger = logging.getLogger(__name__)

# Custom exception for handling data fetch errors
class DataFetchError(Exception):
    pass

def get_crypto_data(symbol, vs_currency='usd', days='365'):
    """
    Fetch historical cryptocurrency price data using the CoinGecko API.

    :param symbol: The symbol of the cryptocurrency (e.g., 'bitcoin').
    :param vs_currency: The currency to compare against (e.g., 'usd').
    :param days: The number of past days to fetch (e.g., '365' for 1 year).
    :return: A DataFrame with historical price data, or None if the fetch fails.
    :raises: DataFetchError if fetching data fails.
    """
    cg = CoinGeckoAPI()
    try:
        data = cg.get_coin_market_chart_by_id(id=symbol, vs_currency=vs_currency, days=days)
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        logger.info(f"Successfully fetched data for {symbol}. Dataframe contains {len(df)} rows.")
        return df

    except requests.exceptions.RequestException as req_ex:
        logger.error(f"Network error while fetching data for {symbol}: {req_ex}")
        raise DataFetchError(f"Network error occurred while fetching data for {symbol}.")
    
    except ValueError as val_ex:
        logger.error(f"Value error: {val_ex}")
        raise DataFetchError(f"Value error occurred while processing data for {symbol}.")
    
    except KeyError as key_ex:
        logger.error(f"Unexpected data structure for {symbol}: {key_ex}")
        raise DataFetchError(f"Failed to process data structure for {symbol}.")
    
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching data for {symbol}: {e}")
        raise DataFetchError(f"Unexpected error occurred for {symbol}.")
