# Stock Price Prediction Tool

This project provides tools for fetching stock data, preprocessing it, and training a model to predict future stock prices using LSTM neural networks.

## Features

- Fetch historical stock data using the `yfinance` library.
- Store stock data in a PostgreSQL database.
- Preprocess the data and scale it for training.
- Build and train an LSTM model to predict stock prices.

## Requirements

- Python 3.x
- `yfinance`
- `psycopg2`
- `numpy`
- `pandas`
- `scikit-learn`
- `tensorflow`
- PostgreSQL

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/KunshArora912/Stock-Prediction.git
    cd stock-price-prediction-tool
    ```

2. Install the required packages:
    ```sh
    pip install yfinance psycopg2 numpy pandas scikit-learn tensorflow
    ```

3. Set up your PostgreSQL database and update the `db_config` dictionary in `data_fetch.py` with your database credentials. **Make sure to change the PostgreSQL password**.

## Usage

### Fetching and Storing Stock Data

1. Run the `data_fetch.py` script to fetch and store stock data in the PostgreSQL database:
    ```sh
    python data_fetch.py
    ```

### Preprocessing Data

1. Preprocess the stock data using the functions provided in `data_preprocess.py`. These functions scale the data and create datasets suitable for training the LSTM model.

### Training the Model

1. Run the `model_train.py` script to train the LSTM model and predict stock prices:
    ```sh
    python model_train.py
    ```

### Code Explanation

#### data_fetch.py

- `fetch_stock_data(ticker, start, end)`: Fetches historical stock data for the given ticker between the specified dates.
- `store_stock_data(ticker, data)`: Stores the fetched stock data in the PostgreSQL database.
- `fetch_and_store_stock_data(ticker, start, end)`: Combines the fetch and store operations.

#### data_preprocess.py

- `preprocess_data(data)`: Scales the 'Close' prices of the stock data.
- `create_dataset(data, time_step=60)`: Creates datasets for training the LSTM model, based on a specified time step.

#### model_train.py

- `build_model(input_shape)`: Builds and compiles the LSTM model.
- `process_stock(ticker, start, end)`: Fetches, preprocesses, and trains the model on the stock data. Predicts the stock price for the given ticker.

## Database Setup

1. Create a PostgreSQL database named `stock_data`.
2. Create a table named `stock_prices` with the following structure:
    ```sql
    CREATE TABLE stock_prices (
        ticker VARCHAR(10),
        date DATE,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        PRIMARY KEY (ticker, date)
    );
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


