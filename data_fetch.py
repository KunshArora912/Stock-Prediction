import yfinance as yf
import psycopg2
from psycopg2.extras import execute_batch
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Database connection details
db_config = {
    'dbname': 'stock_data',
    'user': 'postgres',
    'password': '',
    'host': 'localhost'
}


def fetch_stock_data(ticker, start, end):
    logging.info(f'Fetching data for {ticker}')
    data = yf.download(ticker, start=start, end=end)
    return data


def store_stock_data(ticker, data):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Prepare data for insertion
    records = [(ticker, index.date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
               for index, row in data.iterrows()]

    # Insert data into the table
    insert_query = """
    INSERT INTO stock_prices (ticker, date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (ticker, date) DO NOTHING;
    """
    execute_batch(cursor, insert_query, records)

    conn.commit()
    cursor.close()
    conn.close()


def fetch_and_store_stock_data(ticker, start, end):
    data = fetch_stock_data(ticker, start, end)
    if not data.empty:
        store_stock_data(ticker, data)
    return data


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2020-01-01'
    end_date = '2024-07-25'

    for ticker in tickers:
        fetch_and_store_stock_data(ticker, start_date, end_date)
