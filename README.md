# Stock Price Predictor Dashboard

A complete end-to-end stock forecasting project built with Python, Streamlit, Yahoo Finance, Plotly, and Prophet.

## Features

- Enter any supported stock ticker such as `AAPL`, `TSLA`, or `TCS.NS`
- Fetch the last 5 years of historical price data using `yfinance`
- Display interactive historical stock charts with Plotly
- Train a time-series forecasting model with Prophet
- Predict the next 30 days of stock prices
- Show key metrics such as latest close, forecasted close, predicted change, and trend
- Handle invalid ticker errors with clear messages
- Use a loading spinner while fetching data and training the model

## Project Structure

```text
stock-price-predictor-dashboard/
├── app.py
├── data.py
├── model.py
├── utils.py
├── requirements.txt
└── README.md
```

## Installation

```powershell
cd c:\Users\USER\code\python\stock-price-predictor-dashboard
python -m pip install -r requirements.txt
```

## Run the App

```powershell
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## How It Works

1. `data.py` downloads 5 years of historical stock data from Yahoo Finance.
2. `model.py` converts the closing prices into Prophet format using `ds` and `y`.
3. Prophet trains a forecasting model and predicts the next 30 days.
4. `utils.py` creates Plotly charts and dashboard metrics.
5. `app.py` ties everything together in a Streamlit dashboard.

## Dependencies

- streamlit
- pandas
- plotly
- yfinance
- prophet

## Notes

- Yahoo Finance data availability depends on the ticker symbol.
- Prophet forecasting is useful for learning and experimentation, but stock markets are highly uncertain.
- Some Prophet installs may require extra build tools depending on the local environment.
