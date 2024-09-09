import pytest
from unittest.mock import patch, Mock
import pandas as pd
from src.data_fetcher import get_crypto_data

@patch('src.data_fetcher.CoinGeckoAPI')  # Update the mock to CoinGeckoAPI
def test_get_crypto_data_success(mock_coingecko):
    # Mock the return value of the get_coin_market_chart_by_id method
    mock_coingecko_instance = mock_coingecko.return_value
    mock_coingecko_instance.get_coin_market_chart_by_id.return_value = {
        'prices': [
            [1622505600000, 35000],
            [1622592000000, 36000],
        ]
    }
    
    # Expected DataFrame (since CoinGecko only provides price data, we rename 'price' to 'close')
    expected_df = pd.DataFrame({
        'timestamp': pd.to_datetime([1622505600000, 1622592000000], unit='ms'),
        'close': [35000, 36000],
    })
    expected_df.set_index('timestamp', inplace=True)

    # Call the function
    result_df = get_crypto_data('bitcoin')

    # Assertions
    pd.testing.assert_frame_equal(result_df, expected_df)
    mock_coingecko_instance.get_coin_market_chart_by_id.assert_called_once_with(id='bitcoin', vs_currency='usd', days='365')

@patch('src.data_fetcher.CoinGeckoAPI')  # Update the mock to CoinGeckoAPI
def test_get_crypto_data_failure(mock_coingecko):
    # Mock the get_coin_market_chart_by_id method to raise an exception
    mock_coingecko_instance = mock_coingecko.return_value
    mock_coingecko_instance.get_coin_market_chart_by_id.side_effect = Exception("Mocked exception")

    # Call the function, expecting None due to the exception
    result_df = get_crypto_data('bitcoin')

    # Assertions
    assert result_df is None
    mock_coingecko_instance.get_coin_market_chart_by_id.assert_called_once_with(id='bitcoin', vs_currency='usd', days='365')
