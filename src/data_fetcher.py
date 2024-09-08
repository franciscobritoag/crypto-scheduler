import ccxt
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_crypto_data(symbol, timeframe='1d', limit=365):
    try:
        exchange = ccxt.binance()
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None
