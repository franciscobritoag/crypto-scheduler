import pytest
from unittest.mock import patch, Mock
import pandas as pd
from src.forecast import forecast_price

@patch('src.forecast.NeuralProphet')
def test_forecast_price_success(MockNeuralProphet):
    mock_model = MockNeuralProphet.return_value
    mock_model.predict.return_value = pd.DataFrame({
        'ds': pd.date_range(start='2024-08-22', periods=10, freq='D'),
        'yhat': [100 + i for i in range(10)]
    })

    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-08-12', periods=10, freq='D'),
        'close': [100 + i for i in range(10)]
    })

    result = forecast_price(df)

    assert result is not None
    assert 'ds' in result.columns
    assert 'yhat' in result.columns
    assert len(result) == 10

    mock_model.fit.assert_called_once()
    mock_model.predict.assert_called_once()

@patch('src.forecast.NeuralProphet')
def test_forecast_price_failure(MockNeuralProphet):
    mock_model = MockNeuralProphet.return_value
    mock_model.fit.side_effect = Exception("Mocked exception during fit")

    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-08-12', periods=10, freq='D'),
        'close': [100 + i for i in range(10)]
    })

    result = forecast_price(df)
    assert result is None
