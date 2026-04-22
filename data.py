from __future__ import annotations

import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetch the last 5 years of historical stock data from Yahoo Finance.
    """
    if not ticker or not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    stock = yf.Ticker(ticker.strip().upper())
    history = stock.history(period="5y", auto_adjust=False)

    if history.empty:
        raise ValueError(
            f"No data found for ticker '{ticker}'. Please check the symbol and try again."
        )

    history = history.reset_index()

    # Keep only the columns we need and make sure dates are simple timestamps.
    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    available_columns = [column for column in required_columns if column in history.columns]
    history = history[available_columns].copy()
    history["Date"] = pd.to_datetime(history["Date"]).dt.tz_localize(None)

    if "Close" not in history.columns or history["Close"].dropna().empty:
        raise ValueError(f"Closing price data is unavailable for ticker '{ticker}'.")

    return history
