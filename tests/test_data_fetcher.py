import pytest
from unittest.mock import patch, Mock
import pandas as pd
from src.data_fetcher import get_crypto_data

@patch('src.data_fetcher.ccxt.binance')
def test_get_crypto_data_success(mock_binance):
    # Mock the return value of the fetch_ohlcv method
    mock_binance_instance = mock_binance.return_value
    mock_binance_instance.fetch_ohlcv.return_value = [
        [1622505600000, 35000, 36000, 34000, 35500, 100],
        [1622592000000, 35500, 36500, 34500, 36000, 150],
    ]
    
    # Expected DataFrame
    expected_df = pd.DataFrame({
        'timestamp': pd.to_datetime([1622505600000, 1622592000000], unit='ms'),
        'open': [35000, 35500],
        'high': [36000, 36500],
        'low': [34000, 34500],
        'close': [35500, 36000],
        'volume': [100, 150]
    })
    expected_df.set_index('timestamp', inplace=True)

    # Call the function
    result_df = get_crypto_data('BTC/USDT')

    # Assertions
    pd.testing.assert_frame_equal(result_df, expected_df)
    mock_binance_instance.fetch_ohlcv.assert_called_once_with('BTC/USDT', '1d', limit=365)

@patch('src.data_fetcher.ccxt.binance')
def test_get_crypto_data_failure(mock_binance):
    # Mock the fetch_ohlcv method to raise an exception
    mock_binance_instance = mock_binance.return_value
    mock_binance_instance.fetch_ohlcv.side_effect = Exception("Mocked exception")

    # Call the function, expecting None due to the exception
    result_df = get_crypto_data('BTC/USDT')

    # Assertions
    assert result_df is None
    mock_binance_instance.fetch_ohlcv.assert_called_once_with('BTC/USDT', '1d', limit=365)
