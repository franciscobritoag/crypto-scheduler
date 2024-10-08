import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from jinja2 import Template
from src.config import SENDGRID_FROM_EMAIL, SENDGRID_TO_EMAIL
from src.data_fetcher import get_crypto_data
from src.forecast import forecast_price
from src.email_sender import send_email
from src.utils import setup_logging

logger = setup_logging()

forecast_template = Template('''
<h3>Forecast for {{ symbol }}:</h3>
<p>Next 10 days:</p>
{{ forecast_html|safe }}
''')

def process_symbol(symbol):
    df = get_crypto_data(symbol)
    if df is not None:
        forecast = forecast_price(df)
        if forecast is not None:
            forecast = forecast.rename(columns={'ds': 'Date', 'yhat1': 'Value'})
            forecast['Value'] = forecast['Value'].apply(lambda x: f"$ {x:.2f}")
            forecast_html = forecast[['Date', 'Value']].to_html(index=False, classes='forecast-table')

            return forecast_template.render(symbol=symbol, forecast_html=forecast_html)
        else:
            logger.error(f"Forecasting failed for {symbol}")
            return f"<h3>Forecasting failed for {symbol}</h3>"
    else:
        logger.error(f"Fetching data failed for {symbol}")
        return f"<h3>Fetching data failed for {symbol}</h3>"

def main():
    start_time = time.time()
    symbols = ['bitcoin', 'ethereum', 'solana']
    results = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_symbol, symbol) for symbol in symbols]
        for future in as_completed(futures):
            results.append(future.result())

    email_content = "\n\n".join(results)
    send_email("Cryptocurrency Forecast", email_content)

    end_time = time.time()
    total_execution_time = end_time - start_time
    logger.info(f"Total execution time: {total_execution_time:.2f} seconds")

if __name__ == "__main__":
    main()
