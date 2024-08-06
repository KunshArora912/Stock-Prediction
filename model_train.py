import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from data_fetch import fetch_and_store_stock_data
from data_preprocess import preprocess_data, create_dataset
import logging

logging.basicConfig(level=logging.INFO)


def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(input_shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def process_stock(ticker, start, end):
    try:
        data = fetch_and_store_stock_data(ticker, start, end)
        if data.empty:
            logging.warning(f'No data for {ticker}')
            return None
        scaled_data, scaler = preprocess_data(data)
        X, y = create_dataset(scaled_data)
        X = X.reshape(X.shape[0], X.shape[1], 1)

        model = build_model(X.shape)
        model.fit(X, y, epochs=10, batch_size=32, verbose=0)

        # Predict
        last_60_days = scaled_data[-60:]
        X_test = np.array([last_60_days])
        X_test = X_test.reshape((1, X_test.shape[1], 1))
        predicted_price = model.predict(X_test)
        predicted_price = scaler.inverse_transform(predicted_price)
        logging.info(f'Predicted Price for {ticker}: {predicted_price[0][0]}')
        return predicted_price[0][0]
    except Exception as e:
        logging.error(f'Error processing {ticker}: {e}')
        return None


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2020-01-01'
    end_date = '2024-07-25'

    for ticker in tickers:
        process_stock(ticker, start_date, end_date)
