from neuralprophet import NeuralProphet
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def forecast_price(df):
    try:
        logger.info("Starting forecast for dataframe with %d rows", len(df))
        df = df.reset_index()
        logger.info("Dataframe index reset. First few rows:\\n%s", df.head())
        
        df = df.rename(columns={'timestamp': 'ds', 'close': 'y'})
        logger.info("Dataframe columns renamed. Columns are now: %s", df.columns)
        
        logger.info("Initializing NeuralProphet model")
        model = NeuralProphet()

        logger.info("Fitting model with data")
        model.fit(df[['ds', 'y']], freq='D')

        logger.info("Creating future dataframe for forecasting")
        future = model.make_future_dataframe(df, periods=10)
        future['y'] = None
        future = future[['ds', 'y']]
        logger.info("Future dataframe created. First few rows:\\n%s", future.head())

        logger.info("Generating forecast")
        forecast = model.predict(future)
        logger.info("Forecast generated. First few rows:\\n%s", forecast.head())
        
        return forecast
    except Exception as e:
        logger.error(f"Error forecasting data: {e}")
        return None